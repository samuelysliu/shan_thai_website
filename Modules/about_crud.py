from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Modules.dbInit import About as AboutModel

# 取得所有 About 資料
def get_about(db: Session):
    try:
        return db.query(AboutModel).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 新增 About 資料
def create_about(db: Session, title_cn: str, content_cn: str, aboutImageUrl: str):
    try:
        new_about = AboutModel(
            title_cn=title_cn,
            content_cn=content_cn,
            aboutImageUrl=aboutImageUrl
        )
        db.add(new_about)
        db.commit()
        db.refresh(new_about)
        return new_about
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 更新 About 資料
def update_about(db: Session, about_id: int, title_cn: str, content_cn: str, aboutImageUrl: str):
    try:
        about = db.query(AboutModel).filter(AboutModel.id == about_id).first()
        if about:
            about.title_cn = title_cn
            about.content_cn = content_cn
            about.aboutImageUrl = aboutImageUrl
            db.commit()
            db.refresh(about)
            return about
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 刪除 About 資料
def delete_about(db: Session, about_id: int):
    try:
        about = db.query(AboutModel).filter(AboutModel.id == about_id).first()
        if about:
            db.delete(about)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
