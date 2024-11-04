from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Banner(BaseModel):
    title: str
    content: str
    buttonText: str
    buttonLink: str
    bannerImageUrl: str
    
class About(BaseModel):
    title: str
    content: str
    aboutImageUrl: str
    
class Product(BaseModel):
    No: int
    title: str
    content: str
    productImageUrl: str
    
class customerSay(BaseModel):
    No: int
    Name: str
    Content: str
    customerImageUrl: str
    
class team(BaseModel):
    No: int
    Name: str
    title: str
    teamImageUrl: str
    
class contact(BaseModel):
    title: str
    content: str
    address: str
    phone: str
    email: str
    
class externalLink(BaseModel):
    No: int
    name: str
    iconImageUrl: str
    show: bool
    
# 取得 Banner 內容
@router.get("/banner")
async def get_banner():
    

# 更新 Banner 內容