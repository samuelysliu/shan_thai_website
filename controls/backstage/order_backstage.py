from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import modules.order_crud as order_db
import modules.product_crud as product_db
import modules.dbConnect as db_connect
from controls.tools import format_to_utc8 as timeformat
from controls.tools import verify_token, adminAutorizationCheck

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


# **根據 OID 查詢單筆訂單**
@router.get("/orders/{order_id}")
async def get_order_by_oid(
    order_id: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    order = order_db.get_order_by_oid(db, oid=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "oid": order.oid,
        "uid": order.uid,
        "totalAmount": order.totalAmount,
        "address": order.address,
        "recipientName": order.recipientName,
        "recipientPhone": order.recipientPhone,
        "recipientEmail": order.recipientEmail,
        "transportationMethod": order.transportationMethod,
        "paymentMethod": order.paymentMethod,
        "note": order.note,
        "status": order.status,
        "created_at": timeformat(order.created_at.isoformat()),
        "updated_at": timeformat(order.updated_at.isoformat()),
        "details": [
            {
                "pid": detail.pid,
                "productNumber": detail.productNumber,
                "price": detail.price,
                "subtotal": detail.subtotal,
            }
            for detail in order.order_details
        ],
    }


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


# **新增訂單**
@router.post("/orders")
async def create_order(
    order: OrderCreate,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    adminAutorizationCheck(token_data.get("isAdmin"))

    if order.useDiscount and (order.discountPrice is None or order.discountPrice <= 0):
        raise HTTPException(status_code=400, detail="Invalid special price")

    for detail in order.order_details:
        product = product_db.get_product_by_id(db, detail.pid)
        if not product or product.remain < detail.productNumber:
            raise HTTPException(
                status_code=400,
                detail=f"Product ID {detail.pid} is out of stock or insufficient quantity",
            )

    for detail in order.order_details:
        product = product_db.get_product_by_id(db, detail.pid)
        updated = product_db.update_partial_product(
            db, detail.pid, {"remain": product.remain - detail.productNumber}
        )
        if not updated:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to update stock for Product ID {detail.pid}",
            )

    created_order = order_db.create_order(
        db,
        uid=order.uid,
        totalAmount=order.totalAmount,
        discountPrice=order.discountPrice or 0,
        useDiscount=order.useDiscount,
        address=order.address,
        recipientName=order.recipientName,
        recipientPhone=order.recipientPhone,
        recipientEmail=order.recipientEmail,
        transportationMethod=order.transportationMethod,
        paymentMethod=order.paymentMethod,
        note=order.note,
        status=order.status,
        order_details=[detail.dict() for detail in order.order_details],
    )
    if not created_order:
        raise HTTPException(status_code=500, detail="Order creation failed")
    return created_order


# 更新訂單
@router.patch("/orders/{oid}")
async def update_order(
    oid: int,
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


# 刪除訂單
@router.delete("/orders/{oid}")
async def delete_order(
    oid: int,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    success = order_db.delete_order(db, oid=oid)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"detail": "Order deleted successfully"}
