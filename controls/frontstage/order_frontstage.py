from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import modules.dbConnect as db_connect
import modules.order_crud as order_db
import modules.product_crud as product_db
import modules.cart_crud as cart_db
import modules.store_selection_crud as store_selection_db
from controls.cash_flow import create_payment_callback_record, create_checkMacValue
from controls.logistic import create_store_logistic_order, create_home_logistic_order

from controls.tools import format_to_utc8 as timeformat
from controls.tools import (
    verify_token,
    userAuthorizationCheck,
    generate_verification_code,
    send_email,
)
from datetime import datetime

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
    address: str
    recipientName: str
    recipientPhone: str
    recipientEmail: str
    transportationMethod: str
    paymentMethod: str
    orderNote: str
    order_details: List[OrderDetailBase]  # 訂單明細


class OrderResponse(OrderBase):
    oid: str
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

    # 創建訂單
    new_order = order_db.create_order(
        db,
        oid=generate_verification_code(10),
        uid=order.uid,
        totalAmount=total_amount,  # 使用後端計算的總金額
        discountPrice=0,
        useDiscount=False,
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

    # 如果是貨到付款，直接建立物流單
    if order.paymentMethod == "貨到付款":
        create_store_logistic_order(
            oid=new_order.oid,
            trade_date=new_order.created_at,
            store_type=new_order.transportationMethod,
            order_amount=new_order.totalAmount,
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

    # 2. 將庫存數量加回
    order_details = order_db.get_order_details_by_oid(db, oid)
    for order_detail in order_details:
        product = product_db.get_product_by_id(db, order_detail.pid)
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product ID {order_detail.pid} not found for restocking",
            )

        # 更新庫存
        update_data = {"remain": product.remain + order_detail.productNumber}
        product_updated = product_db.update_partial_product(
            db, order_detail.pid, update_data
        )
        if not product_updated:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update product remain for Product ID {order_detail.pid}",
            )

    # 3. 更新訂單狀態成為取消
    update_data = {"status": "已取消"}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_order = order_db.update_order(db, oid=oid, updates=update_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


# 更新訂單
@router.put("/orders/{oid}")
async def update_order_status(
    oid: str,
    order: OrderUpdate,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    try:
        # 檢查該訂單是否屬於當前用戶
        check_order = order_db.get_order_by_oid(db, oid)
        if not check_order or check_order["uid"] != token_data.get("uid"):
            raise HTTPException(
                status_code=403, detail="Order not found or access denied"
            )

        # 確認是合法修改的內容
        valid_payment = ["匯款", "貨到付款", None]
        if order.paymentMethod not in valid_payment:
            raise HTTPException(status_code=400, detail="Invalid order payment")

        valid_status = ["待確認", None]
        if order.status not in valid_status:
            raise HTTPException(status_code=400, detail="Invalid order status")

        update_data = order.dict(exclude_unset=True)  # 排除未設置的字段
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        updated_order = order_db.update_order(db, oid=oid, updates=update_data)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")
        return updated_order
    except:
        raise HTTPException(status_code=500, detail="Failed to update the order")


# 接受金流主動回拋訂單資訊
@router.post("/cash_flow_order")
async def received_cash_flow_response(
    MerchantID: str = Form(...),  # 特店編號
    MerchantTradeNo: str = Form(...),  # 特店交易編號
    StoreID: str = Form(None),  # 特店旗下店舖代號
    RtnCode: int = Form(
        ...
    ),  # 交易狀態，若回傳值為1時，為付款成功，若RtnCode為”10300066″ 時，代表交易付款結果待確認中。ATM 回傳值時為2時，交易狀態為取號成功，其餘為失敗。
    RtnMsg: str = Form(...),  # 交易訊息
    TradeNo: str = Form(...),  # 綠界的交易編號
    TradeAmt: int = Form(...),  # 交易金額
    PaymentDate: str = Form(None),  # 付款時間，格式為yyyy/MM/dd HH:mm:ss
    PaymentType: str = Form(...),  # 特店選擇的付款方式
    PaymentTypeChargeFee: int = Form(0),  # 交易手續費金額
    PlatformID: str = Form(None),  # 特約合作平台商代號
    TradeDate: str = Form(...),  # 訂單成立時間，格式為yyyy/MM/dd HH:mm:ss
    SimulatePaid: int = Form(
        1
    ),  # 是否為模擬付款，0：代表此交易非模擬付款。1：代表此交易為模擬付款。
    CheckMacValue: str = Form(...),  # 檢查碼
    BankCode: str = Form(None),  # 繳費銀行代碼
    vAccount: str = Form(None),  # 繳費虛擬帳號
    ExpireDate: str = Form(None),  # 繳費期限，格式為yyyy/MM/dd
    db: Session = Depends(get_db),
):
    params = {
        MerchantID: MerchantID,
        MerchantTradeNo: MerchantTradeNo,
        StoreID: StoreID,
        RtnCode: RtnCode,
        RtnMsg: RtnMsg,
        TradeNo: TradeNo,
        TradeAmt: TradeAmt,
        PaymentDate: PaymentDate,
        PaymentType: PaymentType,
        PaymentTypeChargeFee: PaymentTypeChargeFee,
        PlatformID: PlatformID,
        TradeDate: TradeDate,
        SimulatePaid: SimulatePaid,
    }
    
    if not CheckMacValue == create_checkMacValue(params):
        raise HTTPException(
            status_code=400, detail=f"Invalid Call"
        )
    try:
        new_record = create_payment_callback_record(
            db=db,
            merchant_id=MerchantID,
            merchant_trade_no=MerchantTradeNo,
            store_id=StoreID,
            rtn_code=RtnCode,
            rtn_msg=RtnMsg,
            trade_no=TradeNo,
            trade_amt=TradeAmt,
            payment_date=PaymentDate,
            payment_type=PaymentType,
            payment_type_charge_fee=PaymentTypeChargeFee,
            platform_id=PlatformID,
            trade_date=TradeDate,
            simulate_paid=SimulatePaid,
            check_mac_value=CheckMacValue,
            bank_code=BankCode,
            v_account=vAccount,
            expire_date=ExpireDate,
        )

        if not new_record:
            print("Failed to create payment callback record")
    except:
        print("Failed to create payment callback record")

    try:
        if (PaymentType.__contains__("Credit") and RtnCode == 1) or (
            PaymentType.__contains__("ATM") and RtnCode == 2
        ):
            update_data = {"status": "待出貨"}

            # 建立物流單
            order = order_db.get_order_by_oid(db=db, oid=MerchantTradeNo)
            if (
                order["transportationMethod"] == "seven"
                or order["transportationMethod"] == "family"
            ):
                create_store_logistic_order(
                    oid=MerchantTradeNo,
                    trade_date=TradeDate,
                    store_type=order["transportationMethod"],
                    order_amount=order["totalAmount"],
                    isCollection="N",
                    product="善泰團隊聖物",
                    user_name=order["recipientName"],
                    user_phone=order["recipientPhone"],
                    user_email=order["recipientEmail"],
                    store_id=order["address"],
                )
            else:
                create_home_logistic_order(
                    oid=MerchantTradeNo,
                    trade_date=TradeDate,
                    order_amount=order["totalAmount"],
                    product="善泰團隊聖物",
                    product_weight=order["productWeight"],
                    user_name=order["recipientName"],
                    user_phone=order["recipientPhone"],
                    zip_code=order["zipCode"],
                    address=order["address"],
                    user_email=order["recipientEmail"],
                )

        else:  # 如果訂單被取消，要恢復庫存
            order_details = order_db.get_order_details_by_oid(
                db=db, oid=MerchantTradeNo
            )
            for order_detail in order_details:
                product = product_db.get_product_by_id(db, order_detail.pid)
                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product ID {order_detail.pid} not found for restocking",
                    )

                # 更新庫存
                update_data = {"remain": product.remain + order_detail.productNumber}
                product_updated = product_db.update_partial_product(
                    db, order_detail.pid, update_data
                )
                if not product_updated:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to update product remain for Product ID {order_detail.pid}",
                    )
            update_data = {"status": "已取消"}

        updated_order = order_db.update_order(
            db, oid=MerchantTradeNo, updates=update_data
        )

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

