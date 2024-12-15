from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import modules.external_link_crud as external_link_db
import modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db

# 條款的 Pydantic 模型
class ExternalLink(BaseModel):
    id: int
    name_cn: str
    name_en: str
    iconImageUrl: str
    externalLink: str

    class Config:
        from_attributes = True
        
@router.get("/external_link", response_model=list[ExternalLink])
async def get_all_external_link_isShow(db: Session = Depends(get_db)):
    """
    獲取所有狀態是顯示的外部連結
    """
    external_link = external_link_db.get_external_link_isShow(db)
    if not external_link:
        raise HTTPException(status_code=404, detail="No terms found")
    return external_link