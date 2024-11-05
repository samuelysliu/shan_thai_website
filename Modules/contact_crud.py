from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Modules.dbInit import Contact as ContactModel

# 取得所有 Contact 資料
def get_contact(db: Session):
    try:
        return db.query(ContactModel).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 新增 Contact 資料
def create_contact(db: Session, title_cn: str, content_cn: str, address_cn: str, phone: str, email: str):
    try:
        new_contact = ContactModel(
            title_cn=title_cn,
            content_cn=content_cn,
            address_cn=address_cn,
            phone=phone,
            email=email
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return new_contact
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 更新 Contact 資料
def update_contact(db: Session, contact_id: int, title_cn: str, content_cn: str, address_cn: str, phone: str, email: str):
    try:
        contact = db.query(ContactModel).filter(ContactModel.id == contact_id).first()
        if contact:
            contact.title_cn = title_cn
            contact.content_cn = content_cn
            contact.address_cn = address_cn
            contact.phone = phone
            contact.email = email
            db.commit()
            db.refresh(contact)
            return contact
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 刪除 Contact 資料
def delete_contact(db: Session, contact_id: int):
    try:
        contact = db.query(ContactModel).filter(ContactModel.id == contact_id).first()
        if contact:
            db.delete(contact)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
