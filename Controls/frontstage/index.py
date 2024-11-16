from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import Modules.banner_crud as banner_db
import Modules.about_crud as about_db
import Modules.contact_crud as contact_db
import Modules.external_link_crud as external_link_db
import Modules.product_crud as product_db
import Modules.team_crud as team_db
import Modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db

# 取得所有 Banner 資料
@router.get("/banners")
async def get_banners(db: Session = Depends(get_db)):
    banners = banner_db.get_banner(db)
    if not banners:
        raise HTTPException(status_code=404, detail="Banners not found")
    return banners

# 取得 About 資料
@router.get("/about")
async def get_about(db: Session = Depends(get_db)):
    about = about_db.get_about(db)
    if not about:
        raise HTTPException(status_code=404, detail="About section not found")
    return about

# 取得所有 Product 資料
@router.get("/products")
async def get_products(db: Session = Depends(get_db)):
    products = product_db.get_product_data(db)
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    return products

# 取得所有 Team 資料
@router.get("/team")
async def get_team(db: Session = Depends(get_db)):
    team = team_db.get_team_data(db)
    if not team:
        raise HTTPException(status_code=404, detail="Team members not found")
    return team

# 取得 Contact 資料
@router.get("/contact")
async def get_contact(db: Session = Depends(get_db)):
    contact = contact_db.get_contact(db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact information not found")
    return contact

# 取得所有 External Link 資料
@router.get("/external-links")
async def get_external_links(db: Session = Depends(get_db)):
    external_links = external_link_db.get_external_link(db)
    if not external_links:
        raise HTTPException(status_code=404, detail="External links not found")
    return external_links