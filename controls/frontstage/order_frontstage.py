from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import modules.dbConnect as db_connect
import modules.order_crud as order_db
import modules.product_crud as product_db
import modules.cart_crud as cart_db
from controls.tools import format_to_utc8 as timeformat
from controls.tools import verify_token, userAuthorizationCheck, get_now_time
from controls.cash_flow import create_cash_flow_order

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
    oid: int

    class Config:
        from_attributes = True

# **更新訂單用的 Model**
class OrderUpdate(BaseModel):
    paymentMethod: str | None = None
    status: str | None = None
    

class CashFlowOrder(BaseModel):
    MerchantID: str    #特店編號
    MerchantTradeNo: str  #特店交易編號
    StoreID: str   #特店旗下店舖代號
    RtnCode: int  #交易狀態，若回傳值為1時，為付款成功，若RtnCode為”10300066″ 時，代表交易付款結果待確認中。ATM 回傳值時為2時，交易狀態為取號成功，其餘為失敗。
    RtnMsg: str #交易訊息
    TradeNo:str    #綠界的交易編號
    TradeAmt: int   #交易金額
    PaymentDate: str = None    #付款時間，格式為yyyy/MM/dd HH:mm:ss
    PaymentType: str #特店選擇的付款方式
    PaymentTypeChargeFee: int = 0   #交易手續費金額
    PlatformID: str = None #特約合作平台商代號
    TradeDate: str  #訂單成立時間，格式為yyyy/MM/dd HH:mm:ss
    PlatformID: str = None #特約合作平台商代號
    SimulatePaid: int = 1 #是否為模擬付款，0：代表此交易非模擬付款。1：代表此交易為模擬付款。
    CheckMacValue: str #檢查碼
    BankCode: str = None    #繳費銀行代碼
    vAccount: str = None    #繳費虛擬帳號
    ExpireDate:str = None   #繳費期限，格式為yyyy/MM/dd
    

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
    order_status = "待付款"

    # 創建訂單
    new_order = order_db.create_order(
        db,
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
        status=order_status,
        order_details=order_details,  # 使用後端生成的明細
    )
    
    if order.paymentMethod == "匯款":
        create_cash_flow_order("ATM",)
    else:
        order_status = "待出貨"
    

    if not new_order:
        print("Error Message: Failed to create order")
        return []

    # 清空購物車中對應的項目
    selected_cart_items = cart_db.get_carts_by_user(db, order.uid)
    for cart_item in selected_cart_items:
        for detail in order_details:
            if cart_item["pid"] == detail["pid"]:
                cart_db.remove_cart_item(db, cart_item["cart_id"])

    return new_order


# **取消訂單**
@router.delete("/orders/{oid}")
async def cancel_user_order(
    oid: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    #try:
        # 1. 檢查該訂單是否屬於當前用戶
        order = order_db.get_order_by_oid(db, oid)
        if not order or order["uid"] != token_data.get("uid"):
            raise HTTPException(
                status_code=403, detail="Order not found or access denied"
            )
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
    
    #except:
        #raise HTTPException(status_code=500, detail="Failed to cancel the order")

# 更新訂單
@router.put("/orders/{oid}")
async def update_order_status(
    oid: int,
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

@router.post("/cash_flow_order")
async def received_cash_flow_response(order = CashFlowOrder,token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    
    if order.PaymentType == "Credit" and order.RtnCode == 1:
        return {"detail": "success"}
    elif order.PaymentType == "ATM" and order.RtnCode == 2:
        return {"detail": "success"}
    else:
        return {"detail": "failed"}