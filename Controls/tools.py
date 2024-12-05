from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
import jwt
from functools import wraps
from datetime import datetime
import pytz

# 提取 Bearer Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/v1/login")

SECRET_KEY = "shan_thai_project"
ALGORITHM = "HS256"

def jwt_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, token: str = Depends(oauth2_scheme), **kwargs):
        try:
            # 解碼並驗證 Token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            kwargs["token_data"] = payload  # 將 Token 資料傳遞給目標函數
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await func(*args, **kwargs)
    return wrapper

# 新增管理員角色驗證
def admin_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, token: str = Depends(oauth2_scheme), **kwargs):
        try:
            # 解碼並驗證 Token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            role = payload.get("identity")
            if role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized as admin",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            kwargs["token_data"] = payload  # 將 Token 資料傳遞給目標函數
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await func(*args, **kwargs)
    return wrapper

def format_to_utc8(datetime_str):
    """
    將 ISO 格式的時間字串轉換為 UTC+8 並格式化為 YYYY-MM-DD HH:MM:SS
    """
    try:
        # 將字串解析為 UTC 時間
        utc_time = datetime.fromisoformat(datetime_str).replace(tzinfo=pytz.UTC)

        # 轉換為 UTC+8 時間
        utc8_time = utc_time.astimezone(pytz.timezone("Asia/Taipei"))

        # 格式化為指定格式
        return utc8_time.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"Error formatting time: {e}")
        return None