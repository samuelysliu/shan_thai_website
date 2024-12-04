from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import Modules.product_crud as product_db
import Modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db


@router.get("/product")
async def get_product(db: Session = Depends(get_db)):
    product = product_db.get_product(db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/product/by_tag/{ptid}")
async def get_products_by_tag(ptid: int, db: Session = Depends(get_db)):
    products = product_db.get_products_by_tag(db, ptid)
    if not products:
        raise HTTPException(
            status_code=404, detail=f"No products found for tag ID {ptid}"
        )
    return products
