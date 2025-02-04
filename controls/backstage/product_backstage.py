from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session
import modules.product_crud as product_db
import modules.dbConnect as db_connect
from controls.tools import verify_token, adminAutorizationCheck
import cloudinary
import cloudinary.uploader

import os
from dotenv import load_dotenv

from typing import List

load_dotenv()

router = APIRouter()
get_db = db_connect.get_db

class ProductLaunch(BaseModel):
    launch: bool


class ProductTag(BaseModel):
    productTag: str



# 處理上傳照片
def handleImageUpload(files: List[UploadFile] = File(...)):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )
    
    image_urls = []

    try:
        for file in files:
            upload_result = cloudinary.uploader.upload(
                file.file,
                folder="products",
                public_id=file.filename.split(".")[0],
                resource_type="image",
                overwrite=True,
            )

            
            image_urls.append(upload_result.get("secure_url"))  # 獲取圖片的公開 URL

    except Exception as e:
        print(f"System Log: Image upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")

    return image_urls


# 取得所有產品
@router.get("/product")
async def get_product(token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    product = product_db.get_product_join_tag(db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# 更新指定產品內容
@router.patch("/product/{product_id}")
async def update_partial_product(
    product_id: int,
    title_cn: str = Form(None),
    content_cn: str = Form(None),
    price: int = Form(None),
    remain: int = Form(None),
    ptid: int = Form(None),
    files: List[UploadFile] = File(None), 
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    # 構建要更新的資料
    update_data = {}
    if title_cn is not None:
        update_data["title_cn"] = title_cn
    if content_cn is not None:
        update_data["content_cn"] = content_cn
    if price is not None:
        update_data["price"] = price
    if remain is not None:
        update_data["remain"] = remain
    if ptid is not None:
        update_data["ptid"] = ptid

    if files:
        update_data["productImages"] = handleImageUpload(files)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_product = await product_db.update_partial_product(db, product_id, update_data)
    if not updated_product:
        print("System Log: product_backstage API update_partial_product function database query failed")
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


# 建立新產品
@router.post("/product")
async def create_product(
    title_cn: str = Form(...),
    content_cn: str = Form(...),
    price: int = Form(...),
    remain: int = Form(...),
    ptid: int = Form(...),
    files: List[UploadFile] = File(...),
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):

    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    # 先將圖片上傳到cloudinary
    image_urls = handleImageUpload(files)

    # 儲存產品資訊到DB
    created_product = await product_db.create_product(
        db,
        title_cn,
        content_cn,
        price,
        remain,
        ptid,
        images=image_urls,
    )
    if not created_product:
        print("System Log: product_backstage API create_product function database query failed")
        raise HTTPException(status_code=404, detail="Product create failed")
    
    new_product = await product_db.get_product_by_id(db, created_product.pid)
    return new_product


# 上下架指定產品
@router.patch("/product_launch/{product_id}")
async def launch_product(
    product_id: int,
    product: ProductLaunch,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):  
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    # 構建要更新的資料
    update_data = {}
    update_data["launch"] = product.launch
    updated_product = await product_db.update_partial_product(db, product_id, update_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product


# 取得產品清單用的 API
@router.get("/product_list")
async def get_product_list(token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    products = product_db.get_product_join_tag(db)
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")

    data = [
        {
            "pid": product["pid"],
            "productTag": product["productTag"],
            "title_cn": product["title_cn"],
            "title_en": product["title_en"],
            "remain": product["remain"],
            "price": product["price"],
            "specialPrice": product["specialPrice"],
        }
        for product in products
    ]
    return data


# 產品標籤的操作
@router.get("/product_tag")
async def get_product_tag(token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    product_tag = product_db.get_all_product_tags(db)
    if not product_tag:
        print("Product tag not found")
        return []
    return product_tag


@router.post("/product_tag")
def create_tag(tag: ProductTag, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    product_tag = product_db.create_product_tag(db, tag.productTag)
    if not product_tag:
        raise HTTPException(status_code=404, detail="Product tag create failed")

    return product_tag


@router.delete("/product_tag/{tag_id}")
def delete_tag(tag_id: int, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    # 確認是否是管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    product_tag = product_db.delete_product_tag(db, tag_id)
    if not product_tag:
        raise HTTPException(status_code=404, detail="Product tag delete failed")

    return {"detail": "Delete failed"}
