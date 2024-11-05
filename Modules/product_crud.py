from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from Modules.dbInit import Product as ProductModel

# 取得所有 Product 資料
def get_product(db: Session):
    try:
        return db.query(ProductModel).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 新增 Product 資料
def create_product(db: Session, No: int, title_cn: str, content_cn: str, productImageUrl: str):
    try:
        new_product = ProductModel(
            No=No,
            title_cn=title_cn,
            content_cn=content_cn,
            productImageUrl=productImageUrl
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 更新 Product 資料
def update_product(db: Session, product_id: int, No: int, title_cn: str, content_cn: str, productImageUrl: str):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product:
            product.No = No
            product.title_cn = title_cn
            product.content_cn = content_cn
            product.productImageUrl = productImageUrl
            db.commit()
            db.refresh(product)
            return product
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 刪除 Product 資料
def delete_product(db: Session, product_id: int):
    try:
        product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
