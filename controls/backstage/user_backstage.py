from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import modules.user_crud as user_db
import modules.dbConnect as db_connect
from datetime import date
from controls.tools import verify_token, adminAutorizationCheck

router = APIRouter()
get_db = db_connect.get_db


# 定義 Pydantic 模型
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    sex: str | None = None
    star: int | None = 0
    identity: str | None = "user"
    note: str | None = None
    birth_date: date | None = None
    mbti: str | None = None
    phone: str | None = None
    address: str | None = None


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    sex: str | None = None
    star: int | None = None
    identity: str | None = None
    note: str | None = None
    birth_date: date | None = None
    mbti: str | None = None
    phone: str | None = None
    address: str | None = None


# 獲取所有用戶
@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = user_db.get_all_users_with_tokens(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


# 根據用戶 ID 獲取用戶詳情
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_db.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 新增用戶
@router.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    created_user = user_db.create_user(
        db,
        email=user.email,
        username=user.username,
        password=user.password,
        sex=user.sex,
        star=user.star,
        identity="user",
        note=user.note,
        birth_date=user.birth_date,
        mbti=user.mbti,
        phone=user.phone,
        address=user.address
    )
    if not created_user:
        raise HTTPException(status_code=500, detail="User creation failed")
    return created_user


# 更新用戶
@router.patch("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    update_data = user.dict(exclude_unset=True)  # 排除未設置的字段
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_user = user_db.update_user(db, user_id=user_id, updates=update_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# 刪除用戶
@router.delete("/users/{uid}")
async def delete_user(uid: int, db: Session = Depends(get_db)):
    success = user_db.delete_user(db, uid=uid)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted successfully"}


# 取得用戶清單
@router.get("/users_list")
async def get_users(db: Session = Depends(get_db)):
    users = user_db.get_user_list(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users
