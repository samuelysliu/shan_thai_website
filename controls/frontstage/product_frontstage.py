from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import modules.product_crud as product_db
import modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db

# 取得所有上架產品的資訊
@router.get("/product")
async def get_product(db: Session = Depends(get_db)):
    product = product_db.get_product_launch(db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 取得特定產品詳情
@router.get("/product_by_pid/{pid}")
async def get_product(pid: int, db: Session = Depends(get_db)):
    product = product_db.get_product_by_id(db, pid)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 取得所有標籤類別底下的產品
@router.get("/product_by_tag/{ptid}")
async def get_products_by_tag(ptid: int, db: Session = Depends(get_db)):
    if ptid == -1:
        products = product_db.get_product_launch(db)
    else:
        product_list = product_db.get_products_by_tag(db, ptid)
        products = []
        for i in product_list:
            if i["launch"]:
                products.append(i)
                
    if not products:
        print(f"System Log: No products found for tag ID {ptid}")
        return []
    return products

# 取得所有標籤
@router.get("/product_tag")
async def get_product_tag(db: Session = Depends(get_db)):
    product_tag = product_db.get_all_product_tags(db)
    if not product_tag:
        print("Product tag not found")
        return []
    return product_tag
