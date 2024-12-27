from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import modules.dbConnect as db_connect
import modules.user_crud as user_db
import modules.user_verify_crud as user_verify_db
from bcrypt import hashpw, gensalt, checkpw
import os
import jwt
from datetime import datetime, timedelta
from controls.tools import (
    verify_token,
    userAuthorizationCheck,
    send_email,
    generate_verification_code,
)
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("WEBSITE_URL")

# jwt setting
SECRET_KEY = "shan_thai_project"
ALGORITHM = "HS256"  # JWT 加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # Token 的有效期（分鐘）

router = APIRouter()
get_db = db_connect.get_db


# 註冊用模型
class UserBase(BaseModel):
    email: EmailStr
    username: str | None = ""
    sex: str | None = None
    star: int | None = 0
    note: str | None = None

    class Config:
        from_attributes = True


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
    new_password: str


class GoogleUserBase(BaseModel):
    token: str


# 生成 JWT token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 給email跟google登入用的 function
def loginFunction(existing_user):
    if existing_user.identity != "admin":
        isAdmin = False
    else:
        isAdmin = True

    # 生成 JWT token
    access_token = create_access_token(
        data={
            "uid": existing_user.uid,
            "email": existing_user.email,
            "username": existing_user.username,
            "sex": existing_user.sex,
            "star": existing_user.star,
            "isAdmin": isAdmin,
        }
    )

    return {
        "detail": {
            "uid": existing_user.uid,
            "email": existing_user.email,
            "username": existing_user.username,
            "sex": existing_user.sex,
            "isAdmin": isAdmin,
            "token": access_token,
        }
    }


# 註冊 API
@router.post("/register")
async def register_user(user: UserRegistration, db: Session = Depends(get_db)):
    # 檢查用戶是否已存在
    existing_user = user_db.get_user_by_email(db, user.email)
    if existing_user:
        if existing_user.identity != "unauth":
            return {"detail": "Email is already registered"}
        else:
            # 查詢驗證碼
            verification_entry = user_verify_db.get_latest_verification_code(db, existing_user.uid)
            if not verification_entry:
                pass

            # 如果驗證碼還沒過期，叫他檢查 Email
            if verification_entry.expires_at > datetime.utcnow():
                raise {"detail": "Please check Email"}

    # 雜湊密碼
    hashed_password = hashpw(user.password.encode("utf-8"), gensalt()).decode("utf-8")

    # 創建用戶
    new_user = user_db.create_user(
        db,
        email=user.email,
        username=user.username,
        password=hashed_password,
        identity="unauth",
    )

    if not new_user:
        raise HTTPException(status_code=500, detail="Failed to create user")

    verification_code = generate_verification_code()
    
    # 將驗證碼存入資料庫
    verification_entry = user_verify_db.create_verification_code(
        db,
        uid=new_user.uid,
        verification_code=verification_code
    )

    if not verification_entry:
        raise HTTPException(status_code=500, detail="Failed to create verification code")
    
    verify_page = f"{endpoint}/profile/verify/{verification_code}"
    subject = "善泰團隊網站註冊驗證碼"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title>善泰團隊網站註冊驗證碼</title>

    <style type="text/css">
            .rollover:hover .rollover-first {{
                max-height:0px!important;
                display:none!important;
            }}
            .rollover:hover .rollover-second {{
                max-height:none!important;
                display:block!important;
            }}
            .rollover span {{
                font-size:0px;
            }}
            u + .body img ~ div div {{
                display:none;
            }}
            #outlook a {{
                padding:0;
            }}
            span.MsoHyperlink,
            span.MsoHyperlinkFollowed {{
                color:inherit;
                mso-style-priority:99;
            }}
            a.es-button {{
                mso-style-priority:100!important;
                text-decoration:none!important;
            }}
            a[x-apple-data-detectors],
            #MessageViewBody a {{
                color:inherit!important;
                text-decoration:none!important;
                font-size:inherit!important;
                font-family:inherit!important;
                font-weight:inherit!important;
                line-height:inherit!important;
            }}
            .es-desk-hidden {{
                display:none;
                float:left;
                overflow:hidden;
                width:0;
                max-height:0;
                line-height:0;
                mso-hide:all;
            }}
            @media only screen and (max-width:600px) {{
                .es-m-p0r {{ padding-right:0px!important }}
                *[class="gmail-fix"] {{ display:none!important }}
                p, a {{ line-height:150%!important }}
                h1, h1 a {{ line-height:120%!important }}
                h2, h2 a {{ line-height:120%!important }}
                h3, h3 a {{ line-height:120%!important }}
                h4, h4 a {{ line-height:120%!important }}
                .adapt-img {{ width:100%!important; height:auto!important }}
            }}
        </style>
    </head>
    <body class="body" style="width:100%;height:100%;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0">
    <div dir="ltr" class="es-wrapper-color" lang="zh" style="background-color:#FAFAFA">
                <v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
                    <v:fill type="tile" color="#fafafa"></v:fill>
                </v:background>
    <table width="100%" cellspacing="0" cellpadding="0" class="es-wrapper" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#FAFAFA">
        <tr>
        <td valign="top" style="padding:0;Margin:0">
        <table cellpadding="0" cellspacing="0" align="center" class="es-content" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
            <tr>
            <td align="center" class="es-info-area" style="padding:0;Margin:0">
            <table align="center" cellpadding="0" cellspacing="0" bgcolor="#00000000" class="es-content-body" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px" role="none">
            </table></td>
            </tr>
        </table>
        <table cellpadding="0" cellspacing="0" align="center" class="es-header" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" class="es-header-body" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px">
                <tr>
                <td align="left" style="Margin:0;padding-top:10px;padding-right:20px;padding-bottom:10px;padding-left:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td valign="top" align="center" class="es-m-p0r" style="padding:0;Margin:0;width:560px">
                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-bottom:20px;font-size:0px"><img src="https://fpgqzrv.stripocdn.email/content/guids/CABINET_7db6159cc290de9c052d910f3f682ad978dde23fed927ab9de64f992d6f4b4dd/images/shanthaiicon.jpg" alt="Logo" width="100" title="Logo" class="adapt-img" style="display:block;font-size:12px;border:0;outline:none;text-decoration:none"></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table cellpadding="0" cellspacing="0" align="center" class="es-content" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" class="es-content-body" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                <tr>
                <td align="left" style="Margin:0;padding-right:20px;padding-bottom:10px;padding-left:20px;padding-top:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="center" valign="top" style="padding:0;Margin:0;width:560px">
                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-bottom:10px"><h1 class="es-m-txt-c" style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:70px;font-style:normal;font-weight:bold;line-height:70px;color:#333333">善泰團隊</h1></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
                <tr>
                <td align="left" style="Margin:0;padding-top:10px;padding-right:20px;padding-bottom:10px;padding-left:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="center" valign="top" style="padding:0;Margin:0;width:560px">
                    <table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:separate;border-spacing:0px;border-left:2px dashed #cccccc;border-right:2px dashed #cccccc;border-top:2px dashed #cccccc;border-bottom:2px dashed #cccccc;border-radius:5px" role="presentation">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-right:20px;padding-left:20px;padding-top:20px"><h2 class="es-m-txt-c" style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:26px;font-style:normal;font-weight:bold;line-height:31.2px;color:#333333">請點擊下方超連結登入</h2></td>
                        </tr>
                        <tr>
                        <td align="center" style="Margin:0;padding-top:10px;padding-right:20px;padding-left:20px;padding-bottom:20px"><h1 class="es-m-txt-c" style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:46px;font-style:normal;font-weight:bold;line-height:55.2px;color:#333333"><strong>
                            <a target="_blank" style="mso-line-height-rule:exactly;text-decoration:none;color:#5C68E2;font-size:46px" href={verify_page}>
                                點我驗證
                            </a>
                        </strong></h1></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table>
        <table cellpadding="0" cellspacing="0" align="center" class="es-footer" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
            <td align="center" style="padding:0;Margin:0">
            <table align="center" cellpadding="0" cellspacing="0" class="es-footer-body" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:640px" role="none">
                <tr>
                <td align="left" style="Margin:0;padding-right:20px;padding-left:20px;padding-bottom:20px;padding-top:20px">
                <table cellpadding="0" cellspacing="0" width="100%" role="none" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                    <tr>
                    <td align="left" style="padding:0;Margin:0;width:600px">
                    <table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-top:15px;padding-bottom:15px;font-size:0">
                        <table cellpadding="0" cellspacing="0" class="es-table-not-adapt es-social" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                            <tr>
                            <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://www.facebook.com/people/%E5%96%84%E6%B3%B0%E5%9C%98%E9%9A%8A-%E6%B3%B0%E5%9C%8B%E5%8D%97%E5%82%B3%E8%81%96%E7%89%A9%E8%AB%8B%E4%BE%9B/61553678884399/" style="mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Facebook" src="https://fpgqzrv.stripocdn.email/content/assets/img/social-icons/logo-black/facebook-logo-black.png" alt="Fb" width="32" style="display:block;font-size:14px;border:0;outline:none;text-decoration:none"></a></td>
                            <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://x.com/ShanThai666" style="mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="X" src="https://fpgqzrv.stripocdn.email/content/assets/img/social-icons/logo-black/x-logo-black.png" alt="X" width="32" style="display:block;font-size:14px;border:0;outline:none;text-decoration:none"></a></td>
                            <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://www.instagram.com/shanthaiteam/" style="mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Instagram" src="https://fpgqzrv.stripocdn.email/content/assets/img/social-icons/logo-black/instagram-logo-black.png" alt="Inst" width="32" style="display:block;font-size:14px;border:0;outline:none;text-decoration:none"></a></td>
                            <td align="center" valign="top" style="padding:0;Margin:0;padding-right:40px"><a target="_blank" href="https://www.threads.net/@shanthaiteam" style="mso-line-height-rule:exactly;text-decoration:underline;color:#333333;font-size:12px"><img title="Threads" src="https://fpgqzrv.stripocdn.email/content/assets/img/social-icons/logo-black/threads-logo-black.png" alt="Tr" width="32" style="display:block;font-size:14px;border:0;outline:none;text-decoration:none"></a></td>
                            </tr>
                        </table></td>
                        </tr>
                        <tr>
                        <td align="center" style="padding:0;Margin:0;padding-bottom:35px"><p style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:18px;letter-spacing:0;color:#333333;font-size:12px">丹鳳捷運站步行約2分鐘(採預約制)</p></td>
                        </tr>
                    </table></td>
                    </tr>
                </table></td>
                </tr>
            </table></td>
            </tr>
        </table></td>
        </tr>
    </table>
    </div>
    </body>
    </html>
    """
    send_email(user.email, subject, html_content)
    return {"detail": "User registered successfully"}


@router.get("/verify/{verification_code}")
async def verify_user(verification_code:str, db: Session = Depends(get_db)):
    # 查詢驗證碼
    verification_entry = user_verify_db.get_verification_by_code(db, verification_code)
    if not verification_entry:
        raise HTTPException(status_code=404, detail="Verification code not found")

    # 檢查驗證碼是否過期
    if verification_entry.expires_at < datetime.utcnow():
        raise {"detail": "User verified expired"}

    # 更新用戶身份為 "user"
    updated_user = user_db.update_user(db, verification_entry.uid, {"identity": "user"})
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user identity")
    
    # 刪除該用戶的所有驗證碼
    user_verify_db.delete_all_verifications_for_user(db, verification_entry.uid)

    return {"detail": "User verified successfully"}

# 查看用戶資料
@router.get("/profile")
async def get_user_profile(token_data: dict = Depends(verify_token)):
    user = {
        "email": token_data["email"],
        "username": token_data["username"],
        "sex": token_data["sex"],
    }
    return user


# 修改會員資料
@router.put("/profile", response_model=UserBase)
async def update_user_profile(
    updates: UserBase,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token),
):
    uid = token_data.get("uid")
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
    request: PasswordChangeRequest,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    uid = token_data.get("uid")
    if uid is None:
        raise HTTPException(status_code=400, detail="User ID is required")
    user = user_db.get_user_by_uid(db, uid)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_new_password = hashpw(
        request.new_password.encode("utf-8"), gensalt()
    ).decode("utf-8")
    updated_user = user_db.update_user_password(
        db, uid=uid, new_password=hashed_new_password
    )
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
    if not checkpw(
        user.password.encode("utf-8"), existing_user.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Incorrect password")

    response = loginFunction(existing_user)

    return response


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
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


# 取得 Google OAuth 2.0 登入 URL
@router.post("/login/google")
async def google_login(user: GoogleUserBase, db: Session = Depends(get_db)):
    try:
        # 驗證 Google Token
        user_info = id_token.verify_oauth2_token(
            user.token, requests.Request(), CLIENT_ID
        )

        # 取得使用者資料
        email = user_info.get("email")
        name = user_info.get("name")

        # 檢查用戶是否存在
        existing_user = user_db.get_user_by_email(db, email)
        print(user_info)
        if not existing_user:
            # 自動註冊新使用者
            new_user = user_db.create_user(
                db,
                email=email,
                username=name,
                password="google_user",  # 第三方登入不需要密碼
                identity="user",
            )
            if not new_user:
                raise HTTPException(status_code=500, detail="Failed to create user")

            response = loginFunction(new_user)
            return response

        # 如果用戶已存在，返回登入成功
        response = loginFunction(existing_user)
        return response

    except:
        raise HTTPException(status_code=500, detail="Google 驗證錯誤")
