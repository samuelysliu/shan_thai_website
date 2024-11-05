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

class Banner(BaseModel):
    title_cn: str
    content_cn: str
    buttonText_cn: str
    buttonLink: str
    bannerImageUrl: str
    
class About(BaseModel):
    title_cn: str
    content_cn: str
    aboutImageUrl: str
    
class Product(BaseModel):
    No: int
    title_cn: str
    content_cn: str
    productImageUrl: str
    
class CustomerSay(BaseModel):
    No: int
    name_cn: str
    content_cn: str
    customerImageUrl: str
    
class Team(BaseModel):
    No: int
    name_cn: str
    title_cn: str
    teamImageUrl: str
    
class Contact(BaseModel):
    title_cn: str
    content_cn: str
    address_cn: str
    phone: str
    email: str
    
class ExternalLink(BaseModel):
    No: int
    name_cn: str
    iconImageUrl: str
    show: bool

get_db = db_connect.db_connect()

# Banner 相關
# 取得 Banner 內容
@router.get("/banner")
async def get_banner(db: Session = Depends(get_db)):
    banner = banner_db.get_banner(db)
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return banner

# 更新 Banner 內容
@router.put("/banner")
async def update_banner(banner: Banner, db: Session = Depends(get_db)):
    updated_banner = banner_db.update_banner(
        1,
        banner.title_cn,
        banner.content_cn,
        banner.buttonText_cn,
        banner.buttonLink,
        banner.bannerImageUrl,
        db
    )
    if not updated_banner:
        raise HTTPException(status_code=404, detail="Banner not found")
    return updated_banner

# 新增 Banner 內容
@router.post("/banner")
async def create_banner(banner: Banner, db: Session = Depends(get_db)):
    created_banner = banner_db.create_banner(
        banner.title_cn,
        banner.content_cn,
        banner.buttonText_cn,
        banner.buttonLink,
        banner.bannerImageUrl,
        db
    )
    if not created_banner:
        raise HTTPException(status_code=404, detail="Banner create failed")
    return created_banner

# About 相關
@router.get("/about")
async def get_about(db: Session = Depends(get_db)):
    about = about_db.get_about_data(db)
    if not about:
        raise HTTPException(status_code=404, detail="About not found")
    return about

@router.post("/about")
async def create_about(about: About, db: Session = Depends(get_db)):
    created_about = about_db.create_about_data(
        db,
        about.title_cn,
        about.content_cn,
        about.aboutImageUrl
    )
    if not created_about:
        raise HTTPException(status_code=500, detail="Failed to create about section")
    return created_about

@router.put("/about/{about_id}")
async def update_about(about_id: int, about: About, db: Session = Depends(get_db)):
    updated_about = about_db.update_about_data(
        db,
        about_id,
        about.title_cn,
        about.content_cn,
        about.aboutImageUrl
    )
    if not updated_about:
        raise HTTPException(status_code=404, detail="About not found")
    return updated_about

# Team 相關
@router.get("/team")
async def get_team(db: Session = Depends(get_db)):
    team = team_db.get_team_data(db)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.post("/team")
async def create_team(team: Team, db: Session = Depends(get_db)):
    created_team = team_db.create_team_data(
        db,
        team.No,
        team.name_cn,
        team.title_cn,
        team.teamImageUrl
    )
    if not created_team:
        raise HTTPException(status_code=500, detail="Failed to create team member")
    return created_team

@router.put("/team/{team_id}")
async def update_team(team_id: int, team: Team, db: Session = Depends(get_db)):
    updated_team = team_db.update_team_data(
        db,
        team_id,
        team.No,
        team.name_cn,
        team.title_cn,
        team.teamImageUrl
    )
    if not updated_team:
        raise HTTPException(status_code=404, detail="Team member not found")
    return updated_team

# Contact 相關
@router.get("/contact")
async def get_contact(db: Session = Depends(get_db)):
    contact = contact_db.get_contact_data(db)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.post("/contact")
async def create_contact(contact: Contact, db: Session = Depends(get_db)):
    created_contact = contact_db.create_contact_data(
        db,
        contact.title_cn,
        contact.content_cn,
        contact.address_cn,
        contact.phone,
        contact.email
    )
    if not created_contact:
        raise HTTPException(status_code=500, detail="Failed to create contact")
    return created_contact

@router.put("/contact/{contact_id}")
async def update_contact(contact_id: int, contact: Contact, db: Session = Depends(get_db)):
    updated_contact = contact_db.update_contact_data(
        db,
        contact_id,
        contact.title_cn,
        contact.content_cn,
        contact.address_cn,
        contact.phone,
        contact.email
    )
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

# ExternalLink 相關
@router.get("/external-link")
async def get_external_link(db: Session = Depends(get_db)):
    external_link = external_link_db.get_external_link_data(db)
    if not external_link:
        raise HTTPException(status_code=404, detail="External link not found")
    return external_link

@router.post("/external-link")
async def create_external_link(external_link: ExternalLink, db: Session = Depends(get_db)):
    created_external_link = external_link_db.create_external_link_data(
        db,
        external_link.No,
        external_link.name_cn,
        external_link.iconImageUrl,
        external_link.show
    )
    if not created_external_link:
        raise HTTPException(status_code=500, detail="Failed to create external link")
    return created_external_link

@router.put("/external-link/{external_link_id}")
async def update_external_link(external_link_id: int, external_link: ExternalLink, db: Session = Depends(get_db)):
    updated_external_link = external_link_db.update_external_link_data(
        db,
        external_link_id,
        external_link.No,
        external_link.name_cn,
        external_link.iconImageUrl,
        external_link.show
    )
    if not updated_external_link:
        raise HTTPException(status_code=404, detail="External link not found")
    return updated_external_link