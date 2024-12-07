from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import Cart as CartModel
from typing import List


# 取得某個用戶的所有購物車項目
def get_carts_by_user(db: Session, uid: int) -> List[dict]:
    try:
        carts = db.query(CartModel).filter(CartModel.uid == uid, CartModel.is_active == True).all()
        
        # 格式化返回數據
        formatted_carts = [
            {
                "cart_id": cart.cart_id,
                "uid": cart.uid,
                "pid": cart.pid,
                "quantity": cart.quantity,
                "added_at": cart.added_at,
                "updated_at": cart.updated_at
                
            }
            for cart in carts
        ]
        return formatted_carts
    except SQLAlchemyError as e:
        print(f"Error while fetching carts for user {uid}: {e}")
        return None


# 根據 cart_id 獲取購物車項目
def get_cart_by_id(db: Session, cart_id: int) -> dict:
    try:
        cart = db.query(CartModel).filter(CartModel.cart_id == cart_id, CartModel.is_active == True).first()
        if cart:
            # 格式化返回數據
            return {
                "cart_id": cart.cart_id,
                "uid": cart.uid,
                "pid": cart.pid,
                "quantity": cart.quantity,
                "added_at": cart.added_at,
                "is_active": cart.is_active,
                "updated_at": cart.updated_at,
            }
        return None
    except SQLAlchemyError as e:
        print(f"Error while fetching cart by ID {cart_id}: {e}")
        return None


# 新增購物車項目
def add_to_cart(db: Session, uid: int, pid: int, quantity: int) -> dict:
    try:
        # 檢查是否已有相同產品的購物車項目
        existing_cart = db.query(CartModel).filter(CartModel.uid == uid, CartModel.pid == pid, CartModel.is_active == True).first()
        if existing_cart:
            # 更新數量
            existing_cart.quantity += quantity
            db.commit()
            db.refresh(existing_cart)
            return {
                "cart_id": existing_cart.cart_id,
                "uid": existing_cart.uid,
                "pid": existing_cart.pid,
                "quantity": existing_cart.quantity,
                "added_at": existing_cart.added_at,
                "updated_at": existing_cart.updated_at,
            }

        # 如果沒有，新增新的購物車項目
        new_cart = CartModel(uid=uid, pid=pid, quantity=quantity)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        return {
            "cart_id": new_cart.cart_id,
            "uid": new_cart.uid,
            "pid": new_cart.pid,
            "quantity": new_cart.quantity,
            "added_at": new_cart.added_at,
            "is_active": new_cart.is_active,
            "created_at": new_cart.created_at,
            "updated_at": new_cart.updated_at,
        }
    except SQLAlchemyError as e:
        print(f"Error while adding to cart: {e}")
        return None


# 更新購物車項目（修改商品數量）
def update_cart_item(db: Session, cart_id: int, quantity: int) -> dict:
    try:
        cart = db.query(CartModel).filter(CartModel.cart_id == cart_id, CartModel.is_active == True).first()
        if cart:
            cart.quantity = quantity
            db.commit()
            db.refresh(cart)
            return {
                "cart_id": cart.cart_id,
                "uid": cart.uid,
                "pid": cart.pid,
                "quantity": cart.quantity,
                "added_at": cart.added_at,
                "is_active": cart.is_active,
                "created_at": cart.created_at,
                "updated_at": cart.updated_at,
            }
        return None
    except SQLAlchemyError as e:
        print(f"Error while updating cart item with ID {cart_id}: {e}")
        return None


# 刪除購物車項目（邏輯刪除）
def remove_cart_item(db: Session, cart_id: int) -> bool:
    try:
        cart = db.query(CartModel).filter(CartModel.cart_id == cart_id, CartModel.is_active == True).first()
        if cart:
            cart.is_active = False
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error while removing cart item with ID {cart_id}: {e}")
        return False


# 清空某用戶的購物車
def clear_user_cart(db: Session, uid: int) -> bool:
    try:
        carts = db.query(CartModel).filter(CartModel.uid == uid, CartModel.is_active == True).all()
        if carts:
            for cart in carts:
                cart.is_active = False
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error while clearing cart for user {uid}: {e}")
        return False
