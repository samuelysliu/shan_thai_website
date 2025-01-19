from fastapi import APIRouter, HTTPException, Depends, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import modules.dbConnect as db_connect
import modules.order_crud as order_db
import modules.product_crud as product_db
import modules.cart_crud as cart_db
import modules.store_selection_crud as store_selection_db
import modules.shan_thai_token_crud as shan_thai_token_db
from controls.cash_flow import create_payment_callback_record, create_checkMacValue
from controls.logistic import create_store_logistic_order, create_home_logistic_order
from controls.tools import format_to_utc8 as timeformat
from controls.tools import (
    verify_token,
    userAuthorizationCheck,
    generate_verification_code,
    send_email,
)
from controls.order import cancel_order

from datetime import datetime
import re
import httpx
from urllib.parse import quote
import json

router = APIRouter()
get_db = db_connect.get_db


# **訂單模型**（輸入/輸出）
class OrderDetailBase(BaseModel):
    pid: int
    productNumber: int
    price: int
    subtotal: int


# **訂單模型**
class OrderBase(BaseModel):
    uid: int
    totalAmount: int
    zipCode: str = None
    address: str
    recipientName: str
    recipientPhone: str
    recipientEmail: str
    transportationMethod: str
    paymentMethod: str
    orderNote: str
    shanThaiToken: int = 0
    order_details: List[OrderDetailBase]  # 訂單明細


class OrderResponse(OrderBase):
    oid: str
    discountPrice: int
    useDiscount: bool
    created_at: datetime

    class Config:
        from_attributes = True


# **更新訂單用的 Model**
class OrderUpdate(BaseModel):
    paymentMethod: str | None = None
    status: str | None = None


# **檢視用戶自己的歷史訂單**
@router.get("/orders")
async def get_user_orders(
    uid: int, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    # 驗證用戶
    userAuthorizationCheck(uid, token_data.get("uid"))

    orders = order_db.get_orders_by_uid(db, uid)
    if not orders:
        return []

    for order in orders:
        order["created_at"] = timeformat(order["created_at"].isoformat())
        order["updated_at"] = timeformat(order["updated_at"].isoformat())

    return orders


# 建立新訂單
@router.post("/orders", response_model=OrderResponse)
async def create_user_order(
    order: OrderBase,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是新增本人的訂單
    userAuthorizationCheck(order.uid, token_data.get("uid"))

    total_amount = 0  # 初始化總金額
    order_details = []  # 儲存處理後的訂單明細

    # 確認所有產品是否存在並有足夠庫存，並計算價格
    for detail in order.order_details:
        product = product_db.get_product_by_id(db, detail.pid)
        if not product:
            raise HTTPException(
                status_code=404, detail=f"Product ID {detail.pid} not found"
            )
        if product.remain < detail.productNumber:
            raise HTTPException(
                status_code=400,
                detail=f"Product ID {detail.pid} is out of stock or insufficient quantity",
            )

        # 從資料庫中獲取價格並計算小計
        subtotal = product.price * detail.productNumber
        total_amount += subtotal

        # 添加到訂單明細
        order_details.append(
            {
                "pid": detail.pid,
                "productNumber": detail.productNumber,
                "price": product.price,  # 使用資料庫中的價格
                "subtotal": subtotal,
            }
        )

    # 減少剩餘產品數量
    for detail in order_details:
        update_data = {"remain": product.remain - detail["productNumber"]}
        product_updated = product_db.update_partial_product(
            db, detail["pid"], update_data
        )
        if not product_updated:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update product remain for Product ID {detail['pid']}",
            )

    # 處理訂單狀態
    if order.paymentMethod == "貨到付款":
        status = "待出貨"
    else:
        status = "待確認"

    # 防止惡意訂單，貨到付款不可大於兩萬元
    if order.paymentMethod == "貨到付款" and total_amount > 20000:
        raise HTTPException(
            status_code=500,
            detail=f"error requests",
        )

    # 確認善泰幣餘額足夠
    token_data = shan_thai_token_db.get_token_by_uid(db, order.uid)
    if token_data.balance < order.shanThaiToken:
        raise HTTPException(
            status_code=500,
            detail=f"error requests",
        )
    else:  # 扣除使用的善泰幣
        check_update = shan_thai_token_db.update_token_balance(
            db, order.uid, (token_data.balance - order.shanThaiToken)
        )
        if not check_update:
            raise HTTPException(
                status_code=500,
                detail=f"update shan thai token failed",
            )

    if order.shanThaiToken > 0:
        useDiscount = True
    else:
        useDiscount = False

    # 創建訂單
    new_order = order_db.create_order(
        db,
        oid=generate_verification_code(10),
        uid=order.uid,
        totalAmount=total_amount,  # 使用後端計算的總金額
        discountPrice=(total_amount - order.shanThaiToken),
        useDiscount=useDiscount,
        zipCode=order.zipCode,
        address=order.address,
        recipientName=order.recipientName,
        recipientPhone=order.recipientPhone,
        recipientEmail=order.recipientEmail,
        transportationMethod=order.transportationMethod,
        paymentMethod=order.paymentMethod,
        orderNote=order.orderNote,
        status=status,
        order_details=order_details,  # 使用後端生成的明細
    )

    if not new_order:
        print("Error Message: Failed to create order")
        raise HTTPException(
            status_code=400,
            detail=f"Somethins wrong, please try again later.",
        )
    # 清空購物車中對應的項目
    selected_cart_items = cart_db.get_carts_by_user(db, order.uid)
    for cart_item in selected_cart_items:
        for detail in order_details:
            if cart_item["pid"] == detail["pid"]:
                cart_db.remove_cart_item(db, cart_item["cart_id"])

    # 確認是使用優惠價還是總價創建物流訂單
    if useDiscount:
        order_amount = new_order.discountPrice
    else:
        order_amount = new_order.totalAmount

    # 如果是貨到付款，直接建立物流單
    if order.paymentMethod == "貨到付款":
        create_store_logistic_order(
            oid=new_order.oid,
            trade_date=new_order.created_at,
            store_type=new_order.transportationMethod,
            order_amount=order_amount,
            isCollection="Y",
            product="善泰團隊聖物",
            user_name=new_order.recipientName,
            user_phone=new_order.recipientPhone,
            user_email=new_order.recipientEmail,
            store_id=new_order.address,
        )

    return new_order


# **取消訂單**
@router.delete("/orders/{oid}")
async def cancel_user_order(
    oid: str,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # try:
    # 1. 檢查該訂單是否屬於當前用戶
    order = order_db.get_order_by_oid(db, oid)
    if not order or order["uid"] != token_data.get("uid"):
        raise HTTPException(status_code=403, detail="Order not found or access denied")
    # 檢查訂單狀態是否已取消，避免重複操作
    if order["status"] == "已取消":
        raise HTTPException(status_code=400, detail="Order is already cancelled")

    # 將庫存數量加回、更新庫存
    response = await cancel_order(oid=oid, db=db)
    if response["detail"] == "success":
        return response["data"]
    else:
        raise HTTPException(status_code=500, detail=response["detail"])


# 接受金流主動回拋訂單資訊
@router.post("/cash_flow_order")
async def received_cash_flow_response(
    # MerchantID: str = Form(...),  # 特店編號
    # MerchantTradeNo: str = Form(...),  # 特店交易編號
    # StoreID: str = Form(None),  # 特店旗下店舖代號
    # RtnCode: int = Form(
    #    ...
    # ),  # 交易狀態，若回傳值為1時，為付款成功，若RtnCode為”10300066″ 時，代表交易付款結果待確認中。ATM 回傳值時為2時，交易狀態為取號成功，其餘為失敗。
    # RtnMsg: str = Form(...),  # 交易訊息
    # TradeNo: str = Form(...),  # 綠界的交易編號
    # TradeAmt: int = Form(...),  # 交易金額
    # PaymentDate: str = Form(None),  # 付款時間，格式為yyyy/MM/dd HH:mm:ss
    # PaymentType: str = Form(...),  # 特店選擇的付款方式
    # PaymentTypeChargeFee: int = Form(0),  # 交易手續費金額
    # PlatformID: str = Form(None),  # 特約合作平台商代號
    # TradeDate: str = Form(...),  # 訂單成立時間，格式為yyyy/MM/dd HH:mm:ss
    # SimulatePaid: int = Form(
    #    1
    # ),  # 是否為模擬付款，0：代表此交易非模擬付款。1：代表此交易為模擬付款。
    # CheckMacValue: str = Form(...),  # 檢查碼
    # CustomField1: str = Form(None),
    # CustomField2: str = Form(None),
    # CustomField3: str = Form(None),
    # CustomField4: str = Form(None),
    # BankCode: str = Form(None),  # 繳費銀行代碼
    # vAccount: str = Form(None),  # 繳費虛擬帳號
    # ExpireDate: str = Form(None),  # 繳費期限，格式為yyyy/MM/dd
    request: Request,
    db: Session = Depends(get_db),
):
    body = await request.form()
    print(dict(body))  # 打印请求体内容
    return "1|OK"
    """
    print(CheckMacValue)

    # 嘗試解碼為 UTF-8
    try:
        # 原始字節數據
        raw_bytes = bytes(RtnMsg, "latin1")
        # 移除不必要的轉義字符（如 \x78）
        cleaned_bytes = re.sub(
            b"\\\\x([0-9a-fA-F]{2})", lambda m: bytes([int(m.group(1), 16)]), raw_bytes
        )
        correct_str = cleaned_bytes.decode("utf-8")
    except:
        correct_str = RtnMsg
        print(f"解碼失敗")

    params = dict(
        {
            "MerchantID": MerchantID,
            "MerchantTradeNo": MerchantTradeNo,
            "StoreID": StoreID,
            "RtnCode": RtnCode,
            "RtnMsg": correct_str,
            "TradeNo": TradeNo,
            "TradeAmt": TradeAmt,
            "PaymentDate": PaymentDate,
            "PaymentType": PaymentType,
            "PaymentTypeChargeFee": PaymentTypeChargeFee,
            "TradeDate": TradeDate,
            "SimulatePaid": SimulatePaid,
            "CustomField1": CustomField1,
            "CustomField2": CustomField2,
            "CustomField3": CustomField3,
            "CustomField4": CustomField4,
        }
    )

    print(create_checkMacValue(params))

    if CheckMacValue != create_checkMacValue(params):
        raise HTTPException(400, "Invaild call")

    print(params)
    try:
        create_payment_callback_record(
            db=db,
            MerchantID=MerchantID,
            MerchantTradeNo=MerchantTradeNo,
            StoreID=StoreID,
            RtnCode=RtnCode,
            RtnMsg=RtnMsg,
            TradeNo=TradeNo,
            TradeAmt=TradeAmt,
            PaymentDate=PaymentDate,
            PaymentType=PaymentType,
            PaymentTypeChargeFee=PaymentTypeChargeFee,
            PlatformID=None,
            TradeDate=TradeDate,
            SimulatePaid=SimulatePaid,
            CheckMacValue=CheckMacValue,
            BankCode=None,
            vAccount=None,
            ExpireDate=None,
        )
    except:
        print("Failed to call create_payment_callback_record")

    try:
        if (
            PaymentType.__contains__("Credit") or PaymentType.__contains__("ATM")
        ) and RtnCode == 1:
            update_data = {"status": "待出貨"}

            # 建立物流單
            order = order_db.get_order_by_oid(db=db, oid=MerchantTradeNo)

            if order["useDiscount"]:
                order_amount = order["discountPrice"]
            else:
                order_amount = order["totalAmount"]

            if (
                order["transportationMethod"] == "seven"
                or order["transportationMethod"] == "family"
            ):
                result = create_store_logistic_order(
                    oid=MerchantTradeNo,
                    trade_date=TradeDate,
                    store_type=order["transportationMethod"],
                    order_amount=order_amount,
                    isCollection="N",
                    product="善泰團隊聖物",
                    user_name=order["recipientName"],
                    user_phone=order["recipientPhone"],
                    user_email=order["recipientEmail"],
                    store_id=order["address"],
                )
            else:
                if order.get("productWeight") == None:
                    product_weight = 5
                else:
                    product_weight = order["productWeight"]

                if order.get("zipCode") == None:
                    zip_code = "0"
                else:
                    zip_code = order["zipCode"]

                result = create_home_logistic_order(
                    oid=MerchantTradeNo,
                    trade_date=TradeDate,
                    order_amount=order_amount,
                    product="善泰團隊聖物",
                    product_weight=product_weight,
                    user_name=order["recipientName"],
                    user_phone=order["recipientPhone"],
                    zip_code=zip_code,
                    address=order["address"],
                    user_email=order["recipientEmail"],
                )

            if result == "failed":
                send_email(
                    "shanthaiteam@gmail.com",
                    f"物流單{MerchantTradeNo}建立失敗，請手動建立",
                    f"<p>物流單{MerchantTradeNo}建立失敗，請手動建立</p>",
                )

            updated_order = order_db.update_order(
                db, oid=MerchantTradeNo, updates=update_data
            )

        else:  # 如果訂單被取消，要恢復庫存
            response = await cancel_order(oid=MerchantTradeNo, db=db)
            if response["detail"] == "success":
                updated_order = response["data"]
            else:
                updated_order = None

        if not updated_order:
            send_email(
                "shanthaiteam@gmail.com",
                f"更新訂單{MerchantTradeNo}失敗，請手動更新",
                f"<p>更新訂單{MerchantTradeNo}失敗，請手動更新</p>",
            )

        return "1|OK"
    except:
        send_email(
            "shanthaiteam@gmail.com",
            f"更新訂單{MerchantTradeNo}失敗，請手動更新",
            f"<p>更新訂單{MerchantTradeNo}失敗，請手動更新</p>",
        )
        return "1|OK"
    """


# 接收物流商回傳使用者選擇的超商
@router.post("/store_callback")
async def add_store_selection(
    MerchantID: str = Form(...),
    MerchantTradeNo: str = Form(...),
    LogisticsSubType: str = Form(...),
    CVSStoreID: str = Form(...),
    CVSStoreName: str = Form(...),
    CVSAddress: str = Form(...),
    CVSTelephone: str = Form(None),  # 可選欄位
    CVSOutSide: str = Form(None),  # 可選欄位
    ExtraData: str = Form(None),  # 可選欄位
    db: Session = Depends(get_db),
):
    try:
        """
        新增超商選擇記錄
        """
        new_record = store_selection_db.create_store_selection(
            db=db,
            merchant_trade_no=MerchantTradeNo,
            logistics_sub_type=LogisticsSubType,
            cvs_store_id=CVSStoreID,
            cvs_store_name=CVSStoreName,
            cvs_address=CVSAddress,
        )

        if not new_record:
            raise HTTPException(
                status_code=500, detail="Failed to create store selection record"
            )

        # 返回 HTML，讓前端執行關閉分頁操作
        html_content = f"""
        <html>
            <body>
                <script>
                    // 關閉分頁
                    window.close();
                </script>
                <p>Store selection processed successfully. This page will close automatically.</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error processing store selection: {str(e)}"
        )


# 前端頁面詢問使用者選了哪家超商
@router.get("/store_selection/{merchant_trade_no}")
async def get_store_selection(merchant_trade_no: str, db: Session = Depends(get_db)):
    """
    根據 merchant_trade_no 查詢超商選擇記錄
    """
    record = store_selection_db.get_store_selection_by_trade_no(db, merchant_trade_no)

    if not record:
        raise HTTPException(status_code=404, detail="Store selection record not found")

    return {
        "merchant_trade_no": record.merchant_trade_no,
        "logistics_sub_type": record.logistics_sub_type,
        "cvs_store_id": record.cvs_store_id,
        "cvs_store_name": record.cvs_store_name,
        "cvs_address": record.cvs_address,
    }


# 取得地圖API的 keystr
async def get_keystr():
    # 步驟一：呼叫指定的 API
    url = "https://api.tgos.tw/TGOS_API/tgos?ver=2&AppID=x+JLVSx85Lk=&APIKey=in8W74q0ogpcfW/STwicK8D5QwCdddJf05/7nb+OtDh8R99YN3T0LurV4xato3TpL/fOfylvJ9Wv/khZEsXEWxsBmg+GEj4AuokiNXCh14Rei21U5GtJpIkO++Mq3AguFK/ISDEWn4hMzqgrkxNe1Q=="

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        content = response.text

        # 步驟二：從內容中提取 `TGOS.tgHash` 的值
        match = re.search(r'TGOS\.tgHash="([^"]+)"', content)
        if match:
            tg_hash = match.group(1)
            # 將 `tgHash` 使用 `encodeURIComponent` 模擬 URL encode
            keystr = quote(tg_hash, safe="")
            return keystr
        else:
            print("TGOS.tgHash not found in the response.")
            return None
    else:
        print(f"Failed to fetch the API. Status code: {response.status_code}")
        return None


# 判斷地址是否存在
@router.get("/address_exist/{address}")
async def check_address_exist(
    address: str,
    token_data: dict = Depends(verify_token),
):
    keystr = await get_keystr()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://gis.tgos.tw/TGAddress/TGAddress.aspx?oAddress={address}&oSRS=EPSG:3826&oResultDataType=jsonp&keystr={keystr}"
            )
            response_text = response.text

            # 移除 JSONP 包裹，提取 JSON
            if response_text.startswith("var dataObj ="):
                response_text = response_text[len("var dataObj =") :].strip()
                if response_text.endswith(";"):
                    response_text = response_text[:-1]

            data = json.loads(response_text)  # 解析為 Python 字典

            # 檢查地址是否存在
            info = data.get("Info", [{}])[0]

            if info.get("OutTotal", "0") == "0":
                # 地址不存在
                return JSONResponse(
                    status_code=200,
                    content={
                        "success": False,
                    },
                )

            # 地址存在，返回詳細資料
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                },
            )

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"API 請求失敗: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"發生未預期的錯誤: {e}")
