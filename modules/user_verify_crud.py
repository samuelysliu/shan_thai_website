from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import UserVerify
from datetime import datetime, timedelta

# 創建新的驗證碼
def create_verification_code(db: Session, uid: int, verification_code: str, expires_in_minutes: int = 15):
    try:
        expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
        new_verification = UserVerify(
            uid=uid,
            verification_code=verification_code,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )
        db.add(new_verification)
        db.commit()
        db.refresh(new_verification)
        return new_verification
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
    
# 獲取用戶的最新驗證碼
def get_latest_verification_code(db: Session, uid: int):
    try:
        return db.query(UserVerify).filter(UserVerify.uid == uid).order_by(UserVerify.expires_at.desc()).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
    
# 驗證碼是否有效
def is_verification_code_valid(db: Session, uid: int, verification_code: str):
    try:
        verification = db.query(UserVerify).filter(
            UserVerify.uid == uid,
            UserVerify.verification_code == verification_code
        ).order_by(UserVerify.created_at.desc()).first()

        if verification and verification.expires_at > datetime.utcnow():
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
    
# 刪除過期的驗證碼
def delete_expired_verifications(db: Session):
    try:
        db.query(UserVerify).filter(UserVerify.expires_at < datetime.utcnow()).delete()
        db.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
    
# 刪除用戶的所有驗證碼
def delete_all_verifications_for_user(db: Session, uid: int):
    try:
        db.query(UserVerify).filter(UserVerify.uid == uid).delete()
        db.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
    
# 透過驗證碼查詢驗證記錄
def get_verification_by_code(db: Session, verification_code: str):
    try:
        return db.query(UserVerify).filter(UserVerify.verification_code == verification_code).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
