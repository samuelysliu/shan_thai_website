from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import Order, OrderDetail
from typing import List


# 取得所有訂單
def get_all_orders(db: Session) -> List[Order]:
    try:
        return db.query(Order).all()
    except SQLAlchemyError as e:
        print(f"Error while fetching all orders: {e}")
        return []


# 根據 UID 取得訂單（包含訂單明細）
def get_orders_by_uid(db: Session, uid: int) -> List[dict]:
    try:
        orders = (
            db.query(Order)
            .filter(Order.uid == uid)
            .options(joinedload(Order.order_details))
            .order_by(Order.created_at.desc())
            .all()
        )

        formatted_orders = [
            {
                "oid": order.oid,
                "totalAmount": order.totalAmount,
                "discountPrice": order.discountPrice,
                "useDiscount": order.useDiscount,
                "address": order.address,
                "recipientName": order.recipientName,
                "recipientPhone": order.recipientPhone,
                "recipientEmail": order.recipientEmail,
                "transportationMethod": order.transportationMethod,
                "paymentMethod": order.paymentMethod,
                "status": order.status,
                "orderNote": order.orderNote,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "details": [
                    {
                        "quantity": detail.productNumber,
                        "price": detail.price,
                        "title_cn": detail.product.title_cn if detail.product else None,
                        "productImageUrl": (
                            detail.product.productImageUrl if detail.product else None
                        ),
                    }
                    for detail in order.order_details
                ],
            }
            for order in orders
        ]
        return formatted_orders
    except SQLAlchemyError as e:
        print(f"Error while fetching orders for UID {uid}: {e}")
        return []


# 根據 OID 取得單筆訂單（包含訂單明細）
def get_order_by_oid(db: Session, oid: int) -> dict:
    try:
        order = (
            db.query(Order)
            .filter(Order.oid == oid)
            .options(joinedload(Order.order_details))
            .first()
        )
        if not order:
            return None

        return {
            "oid": order.oid,
            "uid": order.uid,
            "totalAmount": order.totalAmount,
            "discountPrice": order.discountPrice,
            "useDiscount": order.useDiscount,
            "address": order.address,
            "recipientName": order.recipientName,
            "recipientPhone": order.recipientPhone,
            "recipientEmail": order.recipientEmail,
            "transportationMethod": order.transportationMethod,
            "paymentMethod": order.paymentMethod,
            "status": order.status,
            "orderNote": order.orderNote,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "details": [
                {
                    "quantity": detail.productNumber,
                    "price": detail.price,
                    "title_cn": detail.product.title_cn if detail.product else None,
                    "productImageUrl": (
                        detail.product.productImageUrl if detail.product else None
                    ),
                }
                for detail in order.order_details
            ],
        }
    except SQLAlchemyError as e:
        print(f"Error while fetching order OID {oid}: {e}")
        return None


# **取得所有訂單及其明細，跨 user 和 product 表**
def get_order_join_user_product(db: Session):
    try:
        # 使用 `joinedload` 預加載 `users` 和 `order_details`，並進一步載入 `product` 關聯數據
        orders = (
            db.query(Order)
            .options(
                joinedload(Order.users),  # 預加載 `users`
                joinedload(Order.order_details).joinedload(OrderDetail.product),  # 預加載 `order_details` 和其關聯的 `product`
            )
            .order_by(Order.created_at.asc())
            .all()
        )

        # 格式化結果
        formatted_orders = [
            {
                "oid": order.oid,
                "uid": order.uid,
                "username": order.users.username if order.users else None,  # 使用者名稱
                "recipientName": order.recipientName,
                "recipientPhone": order.recipientPhone,
                "recipientEmail": order.recipientEmail,
                "address": order.address,
                "transportationMethod": order.transportationMethod,
                "paymentMethod": order.paymentMethod,
                "orderNote": order.orderNote,
                "status": order.status,
                "totalAmount": order.totalAmount,
                "useDiscount": order.useDiscount,
                "discountPrice": order.discountPrice,
                "created_at": order.created_at,
                "updated_at": order.updated_at,
                "details": [
                    {
                        "pid": detail.pid,
                        "productTitle_cn": detail.product.title_cn if detail.product else None,
                        "productNumber": detail.productNumber,
                        "price": detail.price,
                        "subtotal": detail.subtotal,
                    }
                    for detail in order.order_details
                ],
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
    totalAmount: int,
    discountPrice: int,
    useDiscount: bool,
    address: str,
    recipientName: str,
    recipientPhone: str,
    recipientEmail: str,
    transportationMethod: str,
    paymentMethod: str,
    status: str,
    orderNote: str,
    order_details: List[dict],  # 訂單明細資料
) -> Order:
    try:
        new_order = Order(
            uid=uid,
            totalAmount=totalAmount,
            discountPrice=discountPrice,
            useDiscount=useDiscount,
            address=address,
            recipientName=recipientName,
            recipientPhone=recipientPhone,
            recipientEmail=recipientEmail,
            transportationMethod=transportationMethod,
            paymentMethod=paymentMethod,
            status=status,
            orderNote=orderNote,
        )
        db.add(new_order)
        db.commit()

        for detail in order_details:
            new_order_detail = OrderDetail(
                oid=new_order.oid,
                pid=detail["pid"],
                productNumber=detail["productNumber"],
                price=detail["price"],
                subtotal=detail["subtotal"],
            )
            db.add(new_order_detail)

        db.commit()
        db.refresh(new_order)
        return new_order
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error while creating order: {e}")
        return None


# **更新訂單**
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
        db.rollback()
        print(f"Error while updating order OID {oid}: {e}")
        return None


# **刪除訂單（包含訂單明細）**
def delete_order(db: Session, oid: int) -> bool:
    try:
        order = db.query(Order).filter(Order.oid == oid).first()
        if order:
            db.delete(order)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error while deleting order OID {oid}: {e}")
        return False


# **新增訂單明細**
def add_order_detail(
    db: Session, oid: int, pid: int, productNumber: int, price: int, subtotal: int
) -> OrderDetail:
    try:
        new_order_detail = OrderDetail(
            oid=oid,
            pid=pid,
            productNumber=productNumber,
            price=price,
            subtotal=subtotal,
        )
        db.add(new_order_detail)
        db.commit()
        db.refresh(new_order_detail)
        return new_order_detail
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error while adding order detail: {e}")
        return None


# **根據 OID 取得訂單明細**
def get_order_details_by_oid(db: Session, oid: int) -> List[OrderDetail]:
    try:
        return db.query(OrderDetail).filter(OrderDetail.oid == oid).all()
    except SQLAlchemyError as e:
        print(f"Error while fetching order details for OID {oid}: {e}")
        return []


# **刪除訂單明細**
def delete_order_detail(db: Session, odid: int) -> bool:
    try:
        order_detail = db.query(OrderDetail).filter(OrderDetail.odid == odid).first()
        if order_detail:
            db.delete(order_detail)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error while deleting order detail ODID {odid}: {e}")
        return False
