from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from dbInit import Banner as BannerModel



# 取得所有 Banner 資料
def get_banner(db: Session):
    try:
        return db.query(BannerModel).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 根據 ID 取得單個 Banner 資料
def get_single_banner(banner_id: int, db: Session):
    try:
        return db.query(BannerModel).filter(BannerModel.id == banner_id).first()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 新增 Banner 資料
def create_banner(title_cn: str, content_cn: str, buttonText_cn: str, buttonLink: str, bannerImageUrl: str, db: Session):
    try:
        new_banner = BannerModel(
            title_cn=title_cn,
            content_cn=content_cn,
            buttonText_cn=buttonText_cn,
            buttonLink=buttonLink,
            bannerImageUrl=bannerImageUrl
        )
        db.add(new_banner)
        db.commit()
        db.refresh(new_banner)
        return new_banner
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 更新 Banner 資料
def update_banner(banner_id: int, title_cn: str, content_cn: str, buttonText_cn: str, buttonLink: str, bannerImageUrl: str, db: Session):
    try:
        banner = db.query(BannerModel).filter(BannerModel.id == banner_id).first()
        if banner:
            banner.title_cn = title_cn
            banner.content_cn = content_cn
            banner.buttonText_cn = buttonText_cn
            banner.buttonLink = buttonLink
            banner.bannerImageUrl = bannerImageUrl
            db.commit()
            db.refresh(banner)
            return banner
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 刪除 Banner 資料
def delete_banner(banner_id: int, db: Session):
    try:
        banner = db.query(BannerModel).filter(BannerModel.id == banner_id).first()
        if banner:
            db.delete(banner)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
