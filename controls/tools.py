from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Callable
import jwt
from functools import wraps
from datetime import datetime
import pytz
import smtplib
import random
import string
from email.message import EmailMessage


SECRET_KEY = "shan_thai_project"
ALGORITHM = "HS256"
# OAuth2PasswordBearer 用於提取 Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/frontstage/v1/login")

# 驗證並解碼 JWT Token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # 解碼 JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # 返回解碼的 Payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已過期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="無效的認證憑證")


# JWT 驗證裝飾器
def jwt_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, token: str = Depends(oauth2_scheme), **kwargs):
        try:
            # 解碼 JWT Token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token 已過期")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="無效的認證憑證")
        
        # 將解析後的 payload 傳遞給路由
        kwargs["token_data"] = payload
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

# 確認token 跟呼叫API是同一個人
def userAuthorizationCheck(api_uid, token_uId):
    if api_uid != token_uId:
        raise HTTPException(status_code=403, detail="您無權修改此項目")

# 確認是不是管理員
def adminAutorizationCheck(isAdmin):
    if not isAdmin:
        raise HTTPException(status_code=403, detail="您無權修改此項目")
    
# 寄信
def send_email(to_email: str, subject: str, html_content: str):
    # Gmail 設定
    GMAIL_USER = "shanthaiteam@gmail.com"
    GMAIL_PASSWORD = "jrsj qdkn auwf meeg"
    
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content("此電子郵件支援 HTML 格式，請切換至 HTML 檢視。")
    msg.add_alternative(html_content, subtype="html")
    
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email sending failed: {str(e)}")

# 生成隨機驗證碼
def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))