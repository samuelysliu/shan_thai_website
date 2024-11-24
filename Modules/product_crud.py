from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Modules.dbInit import Product as ProductModel
from Modules.dbInit import ProductTag as ProductTagModel


# 取得所有 Product 資料
def get_product(db: Session):
    try:
        return db.query(ProductModel).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 新增 Product 資料
def create_product(
    db: Session,
    title_cn: str,
    content_cn: str,
    price: int,
    remain: int,
    product_tag: int,
    productImageUrl: str,
):
    try:
        new_product = ProductModel(
            title_cn=title_cn,
            content_cn=content_cn,
            price=price,
            remain=remain,
            productTag=product_tag,
            productImageUrl=productImageUrl,
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 更新 Product 資料
def update_partial_product(db: Session, product_id: int, update_data: dict):
    try:
        product = db.query(ProductModel).filter(ProductModel.pid == product_id).first()
        if not product:
            return None

        # 動態更新欄位
        for key, value in update_data.items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        print(f"Error updating product: {e}")
        return None


# 刪除 Product 資料
def delete_product(db: Session, product_id: int):
    try:
        product = db.query(ProductModel).filter(ProductModel.pid == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False


# product tag 操作
def create_product_tag(db: Session, product_tag: str) -> ProductTagModel:
    new_tag = ProductTagModel(productTag=product_tag)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

def get_all_product_tags(db: Session) -> list[ProductTagModel]:
    return db.query(ProductTagModel).all()

def get_product_tag_by_id(db: Session, ptid: int) -> ProductTagModel:
    try:
        return db.query(ProductTagModel).filter(ProductTagModel.ptid == ptid).one()
    except:
        return None

def update_product_tag(db: Session, ptid: int, new_tag: str) -> ProductTagModel:
    tag = db.query(ProductTagModel).filter(ProductTagModel.ptid == ptid).first()
    if tag:
        tag.productTag = new_tag
        db.commit()
        db.refresh(tag)
        return tag
    else:
        return None

def delete_product_tag(db: Session, ptid: int) -> bool:
    tag = db.query(ProductTagModel).filter(ProductTagModel.ptid == ptid).first()
    if tag:
        db.delete(tag)
        db.commit()
        return True
    else:
        return False