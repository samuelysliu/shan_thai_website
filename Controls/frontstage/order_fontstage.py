from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import Modules.dbConnect as db_connect
import Modules.order_crud as order_db

router = APIRouter()
get_db = db_connect.get_db


# **訂單模型**（輸入/輸出）
class OrderBase(BaseModel):
    pid: int
    productNumber: int
    address: str
    transportationMethod: str
    status: str

class OrderResponse(OrderBase):
    oid: int
    uid: int

    class Config:
        from_attributes  = True


# **檢視用戶自己的歷史訂單**
@router.get("/orders", response_model=List[OrderResponse])
async def get_user_orders(uid: int, db: Session = Depends(get_db)):
    orders = order_db.get_orders_by_uid(db, uid)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders


# **新增訂單**
@router.post("/orders", response_model=OrderResponse)
async def create_user_order(order: OrderBase, uid: int, db: Session = Depends(get_db)):
    new_order = order_db.create_order(
        db,
        uid=uid,
        pid=order.pid,
        productNumber=order.productNumber,
        address=order.address,
        transportationMethod=order.transportationMethod,
        status=order.status,
    )
    if not new_order:
        raise HTTPException(status_code=500, detail="Failed to create order")
    return new_order


# **取消訂單**
@router.delete("/orders/{order_id}")
async def cancel_user_order(order_id: int, uid: int, db: Session = Depends(get_db)):
    # 檢查該訂單是否屬於當前用戶
    order = order_db.get_order_by_oid(db, order_id)
    if not order or order.uid != uid:
        raise HTTPException(status_code=403, detail="Order not found or access denied")
    
    # 刪除訂單
    success = order_db.delete_order(db, order_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to cancel order")
    return {"detail": "Order cancelled successfully"}
