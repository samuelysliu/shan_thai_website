from sqlalchemy.orm import Session, joinedload
from modules.dbInit import User
from sqlalchemy.exc import SQLAlchemyError


# 檢查用戶是否存在
def user_exists(db: Session, email: str) -> bool:
    try:
        return db.query(User).filter(User.email == email).first() is not None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False


# 獲取所有用戶
def get_all_users_with_tokens(db: Session):
    try:
        users = db.query(User).options(joinedload(User.shan_thai_tokens)).all()
        result = []
        for user in users:
            token_balance = (
                user.shan_thai_tokens[0].balance if user.shan_thai_tokens else 0
            )
            result.append(
                {
                    "uid": user.uid,
                    "email": user.email,
                    "username": user.username,
                    "sex": user.sex,
                    "star": user.star,
                    "identity": user.identity,
                    "note": user.note,
                    "birth_date": user.birth_date,
                    "mbti": user.mbti,
                    "phone": user.phone,
                    "address": user.address,
                    "referral_code": user.referral_code,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at,
                    "token": token_balance,
                }
            )
        return result
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 取得用戶下拉清單用的SQL
def get_user_list(db: Session):
    try:
        # 查詢指定欄位
        result = db.query(User.uid, User.email, User.username).all()
        # 將結果轉換為字典列表
        return [{"uid": row[0], "email": row[1], "username": row[2]} for row in result]
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 根據 UID 獲取用戶
def get_user_by_uid(db: Session, uid: int):
    try:
        # 查詢 User 並加入 ShanThaiToken 關聯
        user = (
            db.query(User)
            .options(joinedload(User.shan_thai_tokens))  # 加載關聯數據
            .filter(User.uid == uid)
            .first()
        )

        if user:
            # 提取紅利餘額（假設每個用戶最多有一條紅利記錄）
            token_balance = (
                user.shan_thai_tokens[0].balance if user.shan_thai_tokens else 0
            )
            return {
                "uid": user.uid,
                "email": user.email,
                "username": user.username,
                "sex": user.sex,
                "star": user.star,
                "identity": user.identity,
                "note": user.note,
                "birth_date": user.birth_date,
                "mbti": user.mbti,
                "phone": user.phone,
                "address": user.address,
                "referral_code": user.referral_code,
                "token": token_balance,
            }
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 根據 Email 獲取用戶
def get_user_by_email(db: Session, email: str):
    try:
        return db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 創建新用戶
def create_user(
    db: Session,
    email: str,
    username: str,
    password: str,
    identity: str,
    referral_code: str,
    sex: str = None,
    star: int = 0,
    note: str = None,
    birth_date=None,
    mbti=None,
    phone=None,
    address=None,
):
    try:
        new_user = User(
            email=email,
            username=username,
            password=password,
            identity=identity,
            sex=sex,
            star=star,
            note=note,
            birth_date=birth_date,
            mbti=mbti,
            phone=phone,
            address=address,
            referral_code=referral_code
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 更新用戶資料，避免修改敏感字段
def update_user(db: Session, user_id: int, updates: dict):
    try:
        user = db.query(User).filter(User.uid == user_id).first()
        if user:
            for key, value in updates.items():
                if key in {
                    "username",
                    "sex",
                    "star",
                    "note",
                    "identity",
                    "birth_date",
                    "mbti",
                    "phone",
                    "address",
                }:
                    setattr(user, key, value)
            db.commit()
            db.refresh(user)
            return user
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 更新用戶密碼
def update_user_password(db: Session, uid: int, new_password: str):
    try:
        user = db.query(User).filter(User.uid == uid).first()
        if user:
            user.password = new_password
            db.commit()
            db.refresh(user)
            return user
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 刪除用戶
def delete_user(db: Session, uid: int):
    try:
        user = db.query(User).filter(User.uid == uid).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False


# 軟刪除用戶
def soft_delete_user(db: Session, uid: int):
    try:
        user = db.query(User).filter(User.uid == uid).first()
        if user:
            user.identity = "delete"  # 標記為已刪除
            db.commit()
            db.refresh(user)
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
