from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Modules.dbInit import Order
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


# 新增訂單
def create_order(
    db: Session, uid: int, pid: int, productNumber: int, address: str, transportationMethod: str, status: str
) -> Order:
    try:
        new_order = Order(
            uid=uid,
            pid=pid,
            productNumber=productNumber,
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
def update_order(
    db: Session, oid: int, updates: dict
) -> Order:
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
