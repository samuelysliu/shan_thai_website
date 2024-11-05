from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Modules.dbInit import ExternalLink as ExternalLinkModel

# 取得所有 ExternalLink 資料
def get_external_link(db: Session):
    try:
        return db.query(ExternalLinkModel).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 新增 ExternalLink 資料
def create_external_link(db: Session, No: int, name_cn: str, iconImageUrl: str, show: bool):
    try:
        new_external_link = ExternalLinkModel(
            No=No,
            name_cn=name_cn,
            iconImageUrl=iconImageUrl,
            show=show
        )
        db.add(new_external_link)
        db.commit()
        db.refresh(new_external_link)
        return new_external_link
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 更新 ExternalLink 資料
def update_external_link(db: Session, external_link_id: int, No: int, name_cn: str, iconImageUrl: str, show: bool):
    try:
        external_link = db.query(ExternalLinkModel).filter(ExternalLinkModel.id == external_link_id).first()
        if external_link:
            external_link.No = No
            external_link.name_cn = name_cn
            external_link.iconImageUrl = iconImageUrl
            external_link.show = show
            db.commit()
            db.refresh(external_link)
            return external_link
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 刪除 ExternalLink 資料
def delete_external_link(db: Session, external_link_id: int):
    try:
        external_link = db.query(ExternalLinkModel).filter(ExternalLinkModel.id == external_link_id).first()
        if external_link:
            db.delete(external_link)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
