from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import Order
from typing import List


# 取得所有訂單
def get_all_orders(db: Session) -> List[Order]:
    try:
        return db.query(Order).all()
    except SQLAlchemyError as e:
        print(f"Error while fetching all orders: {e}")
        return []


# 根據 UID 取得訂單
def get_orders_by_uid(db: Session, uid: int) -> List[Order]:
    try:
        return db.query(Order).filter(Order.uid == uid).all()
    except SQLAlchemyError as e:
        print(f"Error while fetching orders for UID {uid}: {e}")
        return []


# 根據 OID 取得訂單
def get_order_by_oid(db: Session, oid: int) -> Order:
    try:
        return db.query(Order).filter(Order.oid == oid).first()
    except SQLAlchemyError as e:
        print(f"Error while fetching order OID {oid}: {e}")
        return None


# join product and user 的所有訂單
def get_order_join_user_product(db: Session):
    try:
        # 使用 `joinedload` 一次性載入 `users` 和 `product` 的關聯數據
        orders = (
            db.query(Order)
            .options(
                joinedload(Order.users),  # 預加載 `users`
                joinedload(Order.product),  # 預加載 `product`
            )
            .order_by(Order.created_at.asc())
            .all()
        )

        # 格式化結果，將關聯的 `username` 和 `content_cn` 添加到每個訂單
        formatted_orders = [
            {
                "oid": order.oid,
                "uid": order.uid,
                "username": order.users.username if order.users else None,  # 顧客名稱
                "pid": order.pid,
                "productTitle_cn": (
                    order.product.title_cn if order.product else None
                ),  # 產品描述
                "productNumber": order.productNumber,
                "totalAmount": order.totalAmount,
                "address": order.address,
                "transportationMethod": order.transportationMethod,
                "status": order.status,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
            }
            for order in orders
        ]

        return formatted_orders
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 新增訂單
def create_order(
    db: Session,
    uid: int,
    pid: int,
    productNumber: int,
    totalAmount: int,
    address: str,
    transportationMethod: str,
    status: str,
) -> Order:
    try:
        new_order = Order(
            uid=uid,
            pid=pid,
            productNumber=productNumber,
            totalAmount=totalAmount,
            address=address,
            transportationMethod=transportationMethod,
            status=status,
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except SQLAlchemyError as e:
        print(f"Error while creating order: {e}")
        return None


# 更新訂單
def update_order(db: Session, oid: int, updates: dict) -> Order:
    try:
        order = db.query(Order).filter(Order.oid == oid).first()
        if not order:
            return None

        for key, value in updates.items():
            if hasattr(order, key) and value is not None:
                setattr(order, key, value)

        db.commit()
        db.refresh(order)
        return order
    except SQLAlchemyError as e:
        print(f"Error while updating order OID {oid}: {e}")
        return None


# 刪除訂單
def delete_order(db: Session, oid: int) -> bool:
    try:
        order = db.query(Order).filter(Order.oid == oid).first()
        if order:
            db.delete(order)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error while deleting order OID {oid}: {e}")
        return False
