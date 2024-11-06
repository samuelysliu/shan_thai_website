from sqlalchemy.orm import Session
from Modules.dbInit import User
from sqlalchemy.exc import SQLAlchemyError

# 根據 email 獲取用戶
def get_user_by_email(db: Session, email: str):
    try:
        return db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 創建新用戶
def create_user(db: Session, email: str, username: str, password: str, identity: str):
    try:
        new_user = User(
            email=email,
            username=username,
            password=password,
            identity=identity
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 根據 uid 獲取用戶
def get_user_by_uid(db: Session, uid: int):
    try:
        return db.query(User).filter(User.uid == uid).first()
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
