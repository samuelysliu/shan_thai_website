from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
import jwt
from functools import wraps

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
