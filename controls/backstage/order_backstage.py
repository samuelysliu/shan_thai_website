from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
import modules.order_crud as order_db
import modules.product_crud as product_db
import modules.logistics_order_crud as logistics_order_db
import modules.dbConnect as db_connect
from controls.tools import format_to_utc8 as timeformat
from controls.tools import verify_token, adminAutorizationCheck, get_now_time
from controls.logistic import (
    create_checkMacValue,
    create_store_logistic_order,
    create_home_logistic_order,
)
import controls.logistic as logistic
from datetime import datetime
from controls.order import cancel_order

router = APIRouter()
get_db = db_connect.get_db


# **新增訂單用的 Model**
class OrderDetailCreate(BaseModel):
    pid: int
    productNumber: int
    price: int
    subtotal: int


class OrderCreate(BaseModel):
    uid: int
    totalAmount: int
    discountPrice: int | None = None
    useDiscount: bool = False
    zipCode: str = None
    address: str
    recipientName: str
    recipientPhone: str
    recipientEmail: str
    transportationMethod: str
    paymentMethod: str
    note: str | None = None
    status: str
    order_details: list[OrderDetailCreate]


# **更新訂單用的 Model**
class OrderUpdate(BaseModel):
    totalAmount: int | None = None
    discountPrice: int | None = None
    useDiscount: bool | None = None
    zipCode: str | None = None
    address: str | None = None
    recipientName: str | None = None
    recipientPhone: str | None = None
    recipientEmail: str | None = None
    transportationMethod: str | None = None
    paymentMethod: str | None = None
    note: str | None = None
    status: str | None = None


# **取得所有訂單（包含明細、用戶、產品資訊）**
@router.get("/orders")
async def get_all_orders(
    token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    # 獲取訂單數據
    orders = order_db.get_order_join_user_product(db)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    # 格式化日期
    for order in orders:
        order["created_at"] = timeformat(order["created_at"].isoformat())
        order["updated_at"] = timeformat(order["updated_at"].isoformat())

    return orders


# 根據 UID 查詢用戶的所有訂單
@router.get("/orders/user/{user_id}")
async def get_orders_by_uid(
    user_id: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    orders = order_db.get_orders_by_uid(db, uid=user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders


# 更新訂單
@router.patch("/orders/{oid}")
async def update_order(
    oid: str,
    order: OrderUpdate,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    try:
        # 確認是否是管理員
        adminAutorizationCheck(token_data.get("isAdmin"))
        # 構建要更新的資料
        update_data = order.dict(exclude_unset=True)  # 排除未設置的字段
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        updated_order = order_db.update_order(db, oid=oid, updates=update_data)
        if not updated_order:
            raise HTTPException(status_code=404, detail="Order not found")

        return updated_order
    except:
        raise HTTPException(status_code=500, detail="Failed to cancel the order")


# 取消訂單
@router.delete("/orders/{oid}")
async def cancel_order_api(
    oid: str,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    response = await cancel_order(oid=oid, db=db)
    if response["detail"] == "success":
        return response["data"]
    else:
        raise HTTPException(status_code=500, detail=response["detail"])


# 接收物流商回傳的物流狀態
@router.post("/logistics_callback")
async def received_logistic_response(
    MerchantID: str = Form(...),  # 廠商編號
    MerchantTradeNo: str = Form(...),  # 廠商交易編號
    RtnCode: int = Form(...),  # 物流狀態
    RtnMsg: str = Form(...),  # 物流狀態說明
    AllPayLogisticsID: str = Form(...),  # 綠界物流交易編號
    LogisticsType: str = Form(None),  # 物流類型
    LogisticsSubType: str = Form(None),  # 物流子類型
    GoodsAmount: int = Form(None),  # 商品金額
    UpdateStatusDate: str = Form(None),  # 物流狀態更新時間
    ReceiverName: str = Form(None),  # 收件人姓名
    ReceiverCellPhone: str = Form(None),  # 收件人手機
    ReceiverEmail: str = Form(None),  # 收件人 Email
    ReceiverAddress: str = Form(None),  # 收件人地址
    CVSPaymentNo: str = Form(None),  # 寄貨編號
    CVSValidationNo: str = Form(None),  # 驗證碼
    BookingNote: str = Form(None),  # 托運單號
    CheckMacValue: str = Form(...),  # 檢查碼
    db: Session = Depends(get_db),
):
    """
    ## 物流代號對應表 ##

    商品已送至物流中心
    7-ELEVEN C2C - 2030
    全家 C2C - 3024

    商品已送達門市
    7-ELEVEN C2C - 2073
    全家 C2C - 3018

    消費者成功取件
    7-ELEVEN C2C - 2067
    全家 C2C - 3022

    消費者七天未取件
    7-ELEVEN C2C - 2074
    全家 C2C - 3020
    """
    # 整理回傳的參數
    form_data = {
        "MerchantID": MerchantID,
        "MerchantTradeNo": MerchantTradeNo,
        "RtnCode": RtnCode,
        "RtnMsg": RtnMsg,
        "AllPayLogisticsID": AllPayLogisticsID,
        "LogisticsType": LogisticsType,
        "LogisticsSubType": LogisticsSubType,
        "GoodsAmount": GoodsAmount,
        "UpdateStatusDate": UpdateStatusDate,
        "ReceiverName": ReceiverName,
        "ReceiverCellPhone": ReceiverCellPhone,
        "ReceiverEmail": ReceiverEmail,
        "ReceiverAddress": ReceiverAddress,
        "CVSPaymentNo": CVSPaymentNo,
        "CVSValidationNo": CVSValidationNo,
        "BookingNote": BookingNote,
    }

    # 檢查 CheckMacValue 是否正確
    calculated_mac = create_checkMacValue(form_data)
    if calculated_mac != CheckMacValue:
        raise HTTPException(status_code=400, detail="Invalid CheckMacValue")

    # 轉換 UpdateStatusDate 格式
    try:
        if UpdateStatusDate:
            form_data["UpdateStatusDate"] = datetime.strptime(
                UpdateStatusDate, "%Y/%m/%d %H:%M:%S"
            )
    except ValueError:
        form_data["UpdateStatusDate"] = None

    # 儲存資料至資料庫
    try:
        logistic_record = logistics_order_db.get_logistics_order_by_trade_no(
            db=db, merchant_trade_no=MerchantTradeNo
        )
        if not logistic_record:
            new_record = logistics_order_db.create_logistics_order(
                db=db,
                merchant_trade_no=MerchantTradeNo,
                rtn_code=RtnCode,
                rtn_msg=RtnMsg,
                allpay_logistics_id=AllPayLogisticsID,
                logistics_type=LogisticsType,
                logistics_sub_type=LogisticsSubType,
                goods_amount=GoodsAmount,
                update_status_date=form_data["UpdateStatusDate"],
                receiver_name=ReceiverName,
                receiver_cell_phone=ReceiverCellPhone,
                receiver_email=ReceiverEmail,
                receiver_address=ReceiverAddress,
                cvs_payment_no=CVSPaymentNo,
                cvs_validation_no=CVSValidationNo,
                booking_note=BookingNote,
            )
        else:
            updates = {"RtnCode": RtnCode, "RtnMsg": RtnMsg}
            new_record = logistics_order_db.update_logistics_order_by_trade_no(
                db=db, merchant_trade_no=MerchantTradeNo, updates=updates
            )

        if not new_record:
            raise HTTPException(
                status_code=500, detail="Failed to save logistics order"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if RtnCode == "2030" or RtnCode == "3024":
        update_data = {"status": "配送中"}
    elif RtnCode == "2073" or RtnCode == "3018":
        update_data = {"status": "已送達"}
    elif RtnCode == "2067" or RtnCode == "3022":
        update_data = {"status": "已完成"}
    elif RtnCode == "2074" or RtnCode == "3020":
        update_data = {"status": "已取消"}

    updated_order = order_db.update_order(db, oid=MerchantTradeNo, updates=update_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")

    return "1|OK"


# 回傳託運單所需資料
@router.get("/logistic_print/{oid}")
async def get_logistic_order(
    oid: str,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    try:
        logistic_order = logistics_order_db.get_logistics_order_by_trade_no(
            db=db, merchant_trade_no=oid
        )
        response_dict = {
            "MerchantID": logistic.merchant_id,
            "AllPayLogisticsID": logistic_order.allpay_logistics_id,
            "CVSPaymentNo": logistic_order.cvs_payment_no,
            "CVSValidationNo": logistic_order.cvs_validation_no,
        }
        response_dict["CheckMacValue"] = create_checkMacValue(response_dict)
        return response_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No logistic order: {str(e)}")


# 建立物流單
@router.post("/create_logistics/{oid}")
def create_logistic_order(
    oid: str,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    adminAutorizationCheck(token_data.get("isAdmin"))

    order = order_db.get_order_by_oid(db, oid=oid)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if (
        order["transportationMethod"] == "seven"
        or order["transportationMethod"] == "family"
    ):
        result = create_store_logistic_order(
            oid=oid,
            trade_date=get_now_time(""),
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
        if order.get("productWeight") == None:
            product_weight = 5
        else:
            product_weight = order["productWeight"]

        if order.get("zipCode") == None:
            zip_code = "0"
        else:
            zip_code = order["zipCode"]

        result = create_home_logistic_order(
            oid=oid,
            trade_date=get_now_time(""),
            order_amount=order["totalAmount"],
            product="善泰團隊聖物",
            product_weight=product_weight,
            user_name=order["recipientName"],
            user_phone=order["recipientPhone"],
            zip_code=zip_code,
            address=order["address"],
            user_email=order["recipientEmail"],
        )

    if result["detail"] == "failed":
        return {"detail": "failed"}
    else:
        return {"detail": "success"}
