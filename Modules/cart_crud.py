from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Modules.dbInit import Cart
from typing import List


# 獲取某用戶的所有購物車項目
def get_carts_by_user(db: Session, uid: int) -> List[Cart]:
    try:
        return db.query(Cart).filter(Cart.uid == uid, Cart.is_active == True).all()
    except SQLAlchemyError as e:
        print(f"Error fetching carts for user {uid}: {e}")
        return []


# 根據 cart_id 獲取購物車項目
def get_cart_by_id(db: Session, cart_id: int) -> Cart:
    try:
        return db.query(Cart).filter(Cart.cart_id == cart_id, Cart.is_active == True).first()
    except SQLAlchemyError as e:
        print(f"Error fetching cart {cart_id}: {e}")
        return None


# 新增購物車項目
def add_to_cart(db: Session, uid: int, pid: int, quantity: int) -> Cart:
    try:
        # 檢查是否已有此產品的購物車項目
        existing_cart = db.query(Cart).filter(Cart.uid == uid, Cart.pid == pid, Cart.is_active == True).first()
        if existing_cart:
            # 更新數量
            existing_cart.quantity += quantity
            db.commit()
            db.refresh(existing_cart)
            return existing_cart

        # 如果沒有，新增新的購物車項目
        new_cart = Cart(uid=uid, pid=pid, quantity=quantity)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        return new_cart
    except SQLAlchemyError as e:
        print(f"Error adding to cart: {e}")
        return None


# 更新購物車項目
def update_cart(db: Session, cart_id: int, quantity: int) -> Cart:
    try:
        cart = db.query(Cart).filter(Cart.cart_id == cart_id, Cart.is_active == True).first()
        if cart:
            cart.quantity = quantity
            db.commit()
            db.refresh(cart)
            return cart
        return None
    except SQLAlchemyError as e:
        print(f"Error updating cart {cart_id}: {e}")
        return None


# 刪除購物車項目 (邏輯刪除)
def remove_cart_item(db: Session, cart_id: int) -> bool:
    try:
        cart = db.query(Cart).filter(Cart.cart_id == cart_id).first()
        if cart:
            cart.is_active = False
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error removing cart item {cart_id}: {e}")
        return False


# 清空用戶購物車
def clear_cart_by_user(db: Session, uid: int) -> bool:
    try:
        carts = db.query(Cart).filter(Cart.uid == uid, Cart.is_active == True).all()
        for cart in carts:
            cart.is_active = False
        db.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Error clearing cart for user {uid}: {e}")
        return False
