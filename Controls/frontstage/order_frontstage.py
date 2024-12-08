from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import modules.dbConnect as db_connect
import modules.order_crud as order_db
import modules.product_crud as product_db
import modules.cart_crud as cart_db
from controls.tools import format_to_utc8 as timeformat
from controls.tools import verify_token, userAuthorizationCheck

router = APIRouter()
get_db = db_connect.get_db


# **訂單模型**（輸入/輸出）
class OrderDetailBase(BaseModel):
    pid: int
    productNumber: int
    price: int
    subtotal: int


class OrderBase(BaseModel):
    uid: int
    totalAmount: int
    address: str
    transportationMethod: str
    order_details: List[OrderDetailBase]  # 訂單明細


class OrderResponse(OrderBase):
    oid: int

    class Config:
        from_attributes = True


# **檢視用戶自己的歷史訂單**
@router.get("/orders")
async def get_user_orders(
    uid: int, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    # 驗證用戶
    userAuthorizationCheck(uid, token_data.get("uid"))

    orders = order_db.get_orders_by_uid(db, uid)
    for order in orders:
        order["created_at"] = timeformat(order["created_at"].isoformat())
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders


# **新增訂單**
@router.post("/orders", response_model=OrderResponse)
async def create_user_order(
    order: OrderBase, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    # 確認是新增本人的訂單
    userAuthorizationCheck(order.uid, token_data.get("uid"))

    # 確認所有產品是否有足夠的庫存
    for detail in order.order_details:
        product = product_db.get_product_by_id(db, detail.pid)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {detail.pid} not found")
        if product.remain < detail.productNumber:
            raise HTTPException(
                status_code=400, detail=f"Product ID {detail.pid} is out of stock or insufficient quantity"
            )

    # 減少剩餘產品數量
    for detail in order.order_details:
        product = product_db.get_product_by_id(db, detail.pid)
        update_data = {"remain": product.remain - detail.productNumber}
        product_updated = product_db.update_partial_product(db, detail.pid, update_data)
        if not product_updated:
            raise HTTPException(status_code=500, detail=f"Failed to update product remain for Product ID {detail.pid}")

    # 創建訂單
    new_order = order_db.create_order(
        db,
        uid=order.uid,
        totalAmount=order.totalAmount,
        address=order.address,
        transportationMethod=order.transportationMethod,
        status="待出貨",
        order_details=[
            {
                "pid": detail.pid,
                "productNumber": detail.productNumber,
                "price": detail.price,
                "subtotal": detail.subtotal,
            }
            for detail in order.order_details
        ],
    )
    if not new_order:
        raise HTTPException(status_code=500, detail="Failed to create order")

    # 清空購物車中對應的項目
    selected_cart_items = cart_db.get_carts_by_user(db, order.uid)
    for cart_item in selected_cart_items:
        for detail in order.order_details:
            if cart_item["pid"] == detail.pid:
                cart_db.remove_cart_item(db, cart_item["cart_id"])

    return new_order


# **取消訂單**
@router.delete("/orders/{order_id}")
async def cancel_user_order(
    order_id: int, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    # 檢查該訂單是否屬於當前用戶
    order = order_db.get_order_by_oid(db, order_id)
    if not order or order.uid != token_data.get("uid"):
        raise HTTPException(status_code=403, detail="Order not found or access denied")

    # 刪除訂單及其明細
    success = order_db.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to cancel order")
    return {"detail": "Order cancelled successfully"}
