from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import Terms  # 確保正確導入 Terms 模型

# 新增條款
def create_term(db: Session, name: str, content: str, version: str):
    try:
        new_term = Terms(name=name, content=content, version=version)
        db.add(new_term)
        db.commit()
        db.refresh(new_term)
        return new_term
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        db.rollback()
        return None

# 根據 tid 獲取條款
def get_term_by_id(db: Session, tid: int):
    try:
        return db.query(Terms).filter(Terms.tid == tid).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 獲取所有條款
def get_all_terms(db: Session):
    try:
        return db.query(Terms).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return []

# 更新條款
def update_term(db: Session, tid: int, updates: dict):
    try:
        term = db.query(Terms).filter(Terms.tid == tid).first()
        if term:
            for key, value in updates.items():
                if hasattr(term, key):
                    setattr(term, key, value)
            db.commit()
            db.refresh(term)
            return term
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        db.rollback()
        return None

# 刪除條款
def delete_term(db: Session, tid: int):
    try:
        term = db.query(Terms).filter(Terms.tid == tid).first()
        if term:
            db.delete(term)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        db.rollback()
        return False
