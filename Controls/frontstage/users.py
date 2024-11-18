from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import Modules.dbConnect as db_connect
import Modules.user_crud as user_db
from bcrypt import hashpw, gensalt, checkpw
from requests_oauthlib import OAuth2Session
import os

router = APIRouter()
get_db = db_connect.get_db

# 註冊用模型
class UserBase(BaseModel):
    email: EmailStr
    username: str
    sex: str | None = None
    star: int | None = 0
    note: str | None = None

    class Config:
        orm_mode = True

class UserRegistration(UserBase):
    password: str

# 登入用模型
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 忘記密碼用模型
class PasswordResetRequest(BaseModel):
    email: EmailStr

# 修改密碼用模型
class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str


# 註冊 API
@router.post("/register", response_model=UserBase)
async def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    # 檢查用戶是否已存在
    existing_user = user_db.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    # 雜湊密碼
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt()).decode('utf-8')

    # 創建用戶
    new_user = user_db.create_user(
        db,
        email=user.email,
        username=user.username,
        password=hashed_password,
        identity="user",
    )

    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    return {"detail": "User registered successfully"}

# 查看用戶資料
@router.get("/profile", response_model=UserBase)
async def get_user_profile(db: Session = Depends(get_db), uid: int = None):
    if uid is None:
        raise HTTPException(status_code=400, detail="User ID is required")
    user = user_db.get_user_by_uid(db, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 修改會員資料
@router.put("/profile", response_model=UserBase)
async def update_user_profile(
    updates: UserBase, db: Session = Depends(get_db), uid: int = None
):
    if uid is None:
        raise HTTPException(status_code=400, detail="User ID is required")
    existing_user = user_db.get_user_by_uid(db, uid)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = updates.dict(exclude_unset=True)  # 僅更新提供的字段
    updated_user = user_db.update_user(db, user_id=uid, updates=update_data)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user")
    return updated_user

# 修改密碼
@router.put("/change-password")
async def change_password(
    request: PasswordChangeRequest, db: Session = Depends(get_db), uid: int = None
):
    if uid is None:
        raise HTTPException(status_code=400, detail="User ID is required")
    user = user_db.get_user_by_uid(db, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not checkpw(request.old_password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    hashed_new_password = hashpw(request.new_password.encode("utf-8"), gensalt()).decode(
        "utf-8"
    )
    updated_user = user_db.update_user_password(db, uid=uid, new_password=hashed_new_password)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update password")
    return {"detail": "Password updated successfully"}

# 登入 API
@router.post("/login")
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # 檢查用戶是否存在
    existing_user = user_db.get_user_by_email(db, user.email)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 檢查密碼
    if not checkpw(user.password.encode('utf-8'), existing_user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"detail": "Login successful"}

# 忘記密碼 API
@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    # 檢查用戶是否存在
    user = user_db.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 這裡可以發送一封包含重設密碼連結的電子郵件
    # 請根據你的需求來實作郵件發送功能

    return {"detail": "Password reset link sent to your email"}


# Google OAuth 2.0 設定
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")  # 從你的 .env 文件中讀取
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/frontstage/auth/callback"  # 修改為你的回調 URL
SCOPE = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"

# 取得 Google OAuth 2.0 登入 URL
@router.get("/login/google")
async def google_login():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type="offline")
    return {"authorization_url": authorization_url}

# Google OAuth 2.0 回調
@router.get("/auth/callback")
async def google_callback(db: Session = Depends(get_db), state: str = None, code: str = None):
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    token = google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, code=code)
    
    # 使用訪問令牌請求用戶資料
    response = google.get("https://www.googleapis.com/oauth2/v1/userinfo")
    user_info = response.json()

    # 檢查用戶是否已經存在
    email = user_info.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Failed to retrieve user email from Google")

    existing_user = user_db.get_user_by_email(db, email)
    if not existing_user:
        # 如果用戶不存在，創建新用戶
        new_user = user_db.create_user(
            db,
            email=email,
            username=user_info.get("name"),
            password="",  # 第三方登入不需要密碼
            identity="google"
        )
        if not new_user:
            raise HTTPException(status_code=500, detail="Failed to create user")
    
    return {"detail": "Login successful", "user_info": user_info}