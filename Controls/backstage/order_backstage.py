from fastapi import APIRouter, HTTPException, Depends, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
import Modules.order_crud as order_db
import Modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db


# 新增訂單用的Model
class OrderCreate(BaseModel):
    oid: int
    uid: int
    pid: int
    productNumber: int
    address: str
    transportationMethod: str
    status: str


# 更新訂單用的Model
class OrderUpdate(BaseModel):
    productNumber: int | None = None
    address: str | None = None
    transportationMethod: str | None = None
    status: str | None = None


# 取得所有訂單
@router.get("/orders")
async def get_all_orders(db: Session = Depends(get_db)):
    orders = order_db.get_all_orders(db)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")
    return orders


# 根據 OID 查詢訂單
@router.get("/orders/{order_id}")
async def get_order_by_oid(order_id: int, db: Session = Depends(get_db)):
    order = order_db.get_order_by_oid(db, oid=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# 根據 UID 查詢用戶的所有訂單
@router.get("/orders/user/{user_id}")
async def get_orders_by_uid(user_id: int, db: Session = Depends(get_db)):
    orders = order_db.get_orders_by_uid(db, uid=user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")
    return orders


# 新增訂單
@router.post("/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    created_order = order_db.create_order(
        db,
        uid=order.uid,
        pid=order.pid,
        productNumber=order.productNumber,
        totalAmount=order.totalAmount,
        address=order.address,
        transportationMethod=order.transportationMethod,
        status=order.status,
    )
    if not created_order:
        raise HTTPException(status_code=500, detail="Order creation failed")
    return created_order


# 更新訂單
@router.patch("/orders/{order_id}")
async def update_order(
    order_id: int, order: OrderUpdate, db: Session = Depends(get_db)
):
    # 構建要更新的資料
    update_data = order.dict(exclude_unset=True)  # 排除未設置的字段
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_order = order_db.update_order(db, oid=order_id, updates=update_data)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order


# 刪除訂單
@router.delete("/orders/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    success = order_db.delete_order(db, oid=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}
