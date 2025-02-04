from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import Product as ProductModel
from modules.dbInit import ProductImage as ProductImageModel
from modules.dbInit import ProductTag as ProductTagModel
from typing import List
from functools import lru_cache


# 取得所有 Product 資料
def get_product(db: Session):
    try:
        return db.query(ProductModel).options(joinedload(ProductModel.images)).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 取得所有上架的 Product 資料(不含圖片)
@lru_cache(maxsize=128)
def get_product_launch(db: Session):
    try:
        return db.query(ProductModel).filter(ProductModel.launch == True).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 取得所有 Product 資料並 join product_tag table
def get_product_join_tag(db: Session):
    try:
        # 使用 `joinedload` 來一次性載入 `product_tag` 關聯數據
        products = (
            db.query(ProductModel)
            .options(
                joinedload(ProductModel.product_tag), joinedload(ProductModel.images)
            )
            .all()
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
                "productImageUrl": [image.image_url for image in product.images],
                "launch": product.launch,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
            }
            for product in products
        ]

        return formatted_products
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 根據產品id (pid) 獲取產品圖片
@lru_cache(maxsize=128)
def get_product_image_by_id(db: Session, pid: int):
    try:
        return db.query(ProductImageModel).filter(ProductImageModel.pid == pid).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 根據產品id (pid) 獲取單一產品資料
@lru_cache(maxsize=128)
async def get_product_by_id(db: Session, pid: int):
    try:
        product = (
            db.query(ProductModel)
            .options(
                joinedload(ProductModel.product_tag), joinedload(ProductModel.images)
            )
            .filter(ProductModel.pid == pid)
            .first()
        )
        if not product:
            return None

        return {
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
            "productImageUrl": [
                image.image_url for image in product.images
            ],  # 獲取所有圖片 URL
            "launch": product.launch,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        }
    except SQLAlchemyError as e:
        print(f"Error while fetching product by PID {pid}: {e}")
        return None


# 根據標籤 (ptid) 查詢所有產品(不含圖片)
@lru_cache(maxsize=128)
def get_products_by_tag(db: Session, ptid: int):
    try:
        # 查詢符合 `ptid` 的產品並格式化數據
        products = db.query(ProductModel).filter(ProductModel.ptid == ptid).all()

        # 格式化返回數據
        formatted_products = [
            {
                "pid": product.pid,
                "ptid": product.ptid,
                "title_cn": product.title_cn,
                "title_en": product.title_en,
                "content_cn": product.content_cn,
                "content_en": product.content_en,
                "price": product.price,
                "specialPrice": product.specialPrice,
                "remain": product.remain,
                "sold": product.sold,
                "launch": product.launch,
                "created_at": product.created_at,
                "updated_at": product.updated_at,
            }
            for product in products
        ]
        return formatted_products
    except SQLAlchemyError as e:
        print(f"Error fetching products by tag: {e}")
        return None


# 新增 Product 資料
async def create_product(
    db: Session,
    title_cn: str,
    content_cn: str,
    price: int,
    remain: int,
    ptid: int,
    images: List[str],
):
    try:
        new_product = ProductModel(
            title_cn=title_cn,
            content_cn=content_cn,
            price=price,
            remain=remain,
            ptid=ptid,
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # 儲存多張圖片
        for image_url in images:
            new_image = ProductImageModel(pid=new_product.pid, image_url=image_url)
            db.add(new_image)

        db.commit()
        return new_product
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error: {e}")
        return None


# 更新 Product 資料
async def update_partial_product(db: Session, product_id: int, update_data: dict):
    try:
        product = db.query(ProductModel).filter(ProductModel.pid == product_id).first()
        if not product:
            return None

        # 處理圖片更新
        if "productImages" in update_data:
            db.query(ProductImageModel).filter(
                ProductImageModel.pid == product_id
            ).delete()
            for image_url in update_data["productImages"]:
                new_image = ProductImageModel(pid=product_id, image_url=image_url)
                db.add(new_image)
            db.commit()

        # 動態更新欄位
        for key, value in update_data.items():
            if key != "productImages":
                setattr(product, key, value)

        db.commit()
        db.refresh(product)

        # 使用 joinedload 加載關聯的 productTag
        updated_product = (
            db.query(ProductModel)
            .options(
                joinedload(ProductModel.product_tag), joinedload(ProductModel.images)
            )
            .filter(ProductModel.pid == product_id)
            .first()
        )
        db.commit()
        db.refresh(updated_product)

        # 清除所有快取的數據
        get_product_launch.cache_clear()
        get_product_image_by_id.cache_clear()
        get_product_by_id.cache_clear()
        get_products_by_tag.cache_clear()

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
            "productImageUrl": [image.image_url for image in product.images],
            "launch": updated_product.launch,
            "created_at": updated_product.created_at,
            "updated_at": updated_product.updated_at,
        }
    except Exception as e:
        db.rollback()
        print(f"Error updating product: {e}")
        return None


# 刪除 Product 資料
def delete_product(db: Session, product_id: int):
    try:
        product = db.query(ProductModel).filter(ProductModel.pid == product_id).first()

        # 清除所有快取的數據
        get_product_launch.cache_clear()
        get_product_image_by_id.cache_clear()
        get_product_by_id.cache_clear()
        get_products_by_tag.cache_clear()

        if product:
            db.query(ProductImageModel).filter(
                ProductImageModel.pid == product_id
            ).delete()
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


@lru_cache(maxsize=128)
def get_all_product_tags(db: Session) -> list[ProductTagModel]:
    return db.query(ProductTagModel).all()


def update_product_tag(db: Session, ptid: int, new_tag: str) -> ProductTagModel:
    tag = db.query(ProductTagModel).filter(ProductTagModel.ptid == ptid).first()
    if tag:
        tag.productTag = new_tag
        db.commit()
        db.refresh(tag)

        # 清除所有快取的數據
        get_all_product_tags.cache_clear()

        return tag
    else:
        return None


def delete_product_tag(db: Session, ptid: int) -> bool:
    tag = db.query(ProductTagModel).filter(ProductTagModel.ptid == ptid).first()
    if tag:
        db.delete(tag)
        db.commit()

        # 清除所有快取的數據
        get_all_product_tags.cache_clear()

        return True
    else:
        return False
