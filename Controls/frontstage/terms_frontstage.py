from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import Modules.term_crud as term_db
import Modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db

# 條款的 Pydantic 模型
class Term(BaseModel):
    name: str
    content: str
    version: str

    class Config:
        from_attributes = True
        
@router.get("/terms", response_model=list[Term])
async def get_all_terms(db: Session = Depends(get_db)):
    """
    獲取所有條款
    """
    terms = term_db.get_all_terms(db)
    if not terms:
        raise HTTPException(status_code=404, detail="No terms found")
    return terms