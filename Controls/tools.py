from fastapi import HTTPException, Request
from typing import Callable
import jwt
from functools import wraps
from datetime import datetime
import pytz


SECRET_KEY = "shan_thai_project"
ALGORITHM = "HS256"

def jwt_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Missing or invalid Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = token.split(" ")[1]  # 提取 token
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return await func(*args, token_data=payload, **kwargs)
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

    return wrapper


# 管理員角色驗證
def admin_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        # 从请求头提取 Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authorization header missing or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 提取 token
        token = auth_header.split(" ")[1]

        try:
            # 解码并验证 Token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            role = payload.get("identity")
            if role != "admin":
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized as admin",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            kwargs["token_data"] = payload  # 将 Token 数据传递给目标函数
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError as e:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token: {e}",
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
