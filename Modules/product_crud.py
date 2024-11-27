from sqlalchemy.orm import Session, joinedload
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


# 取得所有 Product 資料並 join product_tag table
def get_product_join_tag(db: Session):
    try:
        # 使用 `joinedload` 來一次性載入 `product_tag` 關聯數據
        products = (
            db.query(ProductModel).options(joinedload(ProductModel.product_tag)).all()
        )

        # 格式化結果，將關聯的 `productTag` 添加到每個產品
        formatted_products = [
            {
                "pid": product.pid,
                "ptid": product.ptid,
                "productTag": (
                    product.product_tag.productTag if product.product_tag else None
                ),
                "title_cn": product.title_cn,
                "title_en": product.title_en,
                "content_cn": product.content_cn,
                "content_en": product.content_en,
                "price": product.price,
                "specialPrice": product.specialPrice,
                "remain": product.remain,
                "sold": product.sold,
                "productImageUrl": product.productImageUrl,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
            }
            for product in products
        ]

        return formatted_products
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
    ptid: int,
    productImageUrl: str,
):
    try:
        new_product = ProductModel(
            title_cn=title_cn,
            content_cn=content_cn,
            price=price,
            remain=remain,
            ptid=ptid,
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

        # 使用 joinedload 加載關聯的 productTag
        updated_product = (
            db.query(ProductModel)
            .options(joinedload(ProductModel.product_tag))
            .filter(ProductModel.pid == product_id)
            .first()
        )
        # 格式化返回數據
        return {
            "pid": updated_product.pid,
            "ptid": updated_product.ptid,
            "productTag": (
                updated_product.product_tag.productTag
                if updated_product.product_tag
                else None
            ),
            "title_cn": updated_product.title_cn,
            "title_en": updated_product.title_en,
            "content_cn": updated_product.content_cn,
            "content_en": updated_product.content_en,
            "price": updated_product.price,
            "specialPrice": updated_product.specialPrice,
            "remain": updated_product.remain,
            "sold": updated_product.sold,
            "productImageUrl": updated_product.productImageUrl,
            "created_at": updated_product.created_at,
            "updated_at": updated_product.updated_at,
        }
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
