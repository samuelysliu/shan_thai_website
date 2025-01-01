from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import ShanThaiToken


# 檢查用戶是否有紅利記錄
def token_exists(db: Session, uid: int) -> bool:
    try:
        return db.query(ShanThaiToken).filter(ShanThaiToken.uid == uid).first() is not None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False


# 獲取所有紅利記錄
def get_all_tokens(db: Session):
    try:
        return db.query(ShanThaiToken).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 根據 UID 獲取用戶紅利記錄
def get_token_by_uid(db: Session, uid: int):
    try:
        return db.query(ShanThaiToken).filter(ShanThaiToken.uid == uid).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 創建用戶紅利記錄
def create_token(db: Session, uid: int, initial_balance: int = 0):
    try:
        new_token = ShanThaiToken(uid=uid, balance=initial_balance)
        db.add(new_token)
        db.commit()
        db.refresh(new_token)
        return new_token
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 更新餘額
def update_token_balance(db: Session, uid: int, new_balance: int):
    try:
        if new_balance < 0:
            raise ValueError("Balance cannot be negative.")
        token = db.query(ShanThaiToken).filter(ShanThaiToken.uid == uid).first()
        if token:
            token.balance = new_balance
            db.commit()
            db.refresh(token)
            return token
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None
    except ValueError as ve:
        print(f"Validation Error: {ve}")
        return None



# 刪除用戶紅利記錄
def delete_token(db: Session, uid: int):
    try:
        token = db.query(ShanThaiToken).filter(ShanThaiToken.uid == uid).first()
        if token:
            db.delete(token)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
