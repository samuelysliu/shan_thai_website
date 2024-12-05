from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import modules.dbConnect as db_connect
import modules.cart_crud as cart_db

router = APIRouter()
get_db = db_connect.get_db


# 用於新增商品至購物車的請求模型
class AddToCartRequest(BaseModel):
    pid: int  # 商品的 ID
    quantity: int  # 商品數量


# 用於更新購物車商品數量的請求模型
class UpdateCartRequest(BaseModel):
    cart_id: int  # 購物車項目的 ID
    quantity: int  # 更新後的商品數量


# 購物車項目的回應模型
class CartItemResponse(BaseModel):
    cart_id: int  # 購物車項目的 ID
    pid: int  # 商品的 ID
    quantity: int  # 商品數量
    added_at: str  # 商品加入購物車的時間
    is_active: bool  # 購物車項目是否有效


# 獲取使用者的購物車所有項目
@router.get("/cart", response_model=List[CartItemResponse])
async def get_user_cart(uid: int, db: Session = Depends(get_db)):
    cart_items = cart_db.get_carts_by_user(db, uid)
    if not cart_items:
        raise HTTPException(status_code=404, detail="找不到購物車項目")
    return cart_items


# 新增商品至購物車
@router.post("/cart", response_model=CartItemResponse)
async def add_to_cart(request: AddToCartRequest, uid: int, db: Session = Depends(get_db)):
    new_cart_item = cart_db.add_to_cart(db, uid=uid, pid=request.pid, quantity=request.quantity)
    if not new_cart_item:
        raise HTTPException(status_code=500, detail="新增購物車項目失敗")
    return new_cart_item


# 更新購物車商品數量
@router.patch("/cart", response_model=CartItemResponse)
async def update_cart_item(request: UpdateCartRequest, uid: int, db: Session = Depends(get_db)):
    # 確保購物車項目屬於該使用者
    cart_item = cart_db.get_cart_by_id(db, request.cart_id)
    if not cart_item or cart_item.uid != uid:
        raise HTTPException(status_code=403, detail="您無權修改此購物車項目")

    updated_cart_item = cart_db.update_cart(db, cart_id=request.cart_id, quantity=request.quantity)
    if not updated_cart_item:
        raise HTTPException(status_code=500, detail="更新購物車項目失敗")
    return updated_cart_item


# 移除購物車中的某一項商品
@router.delete("/cart/{cart_id}")
async def remove_cart_item(cart_id: int, uid: int, db: Session = Depends(get_db)):
    # 確保購物車項目屬於該使用者
    cart_item = cart_db.get_cart_by_id(db, cart_id)
    if not cart_item or cart_item.uid != uid:
        raise HTTPException(status_code=403, detail="您無權移除此購物車項目")

    success = cart_db.remove_cart_item(db, cart_id=cart_id)
    if not success:
        raise HTTPException(status_code=500, detail="移除購物車項目失敗")
    return {"detail": "購物車項目成功移除"}


# 清空使用者的購物車
@router.delete("/cart")
async def clear_cart(uid: int, db: Session = Depends(get_db)):
    success = cart_db.clear_cart_by_user(db, uid)
    if not success:
        raise HTTPException(status_code=500, detail="清空購物車失敗")
    return {"detail": "購物車已成功清空"}
