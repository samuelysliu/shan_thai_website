from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import modules.term_crud as term_db
import modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db

# 條款的 Pydantic 模型
class Term(BaseModel):
    tid: int
    name: str
    content: str
    version: str

    class Config:
        from_attributes = True
        
@router.get("/term_by_id/{tid}", response_model=Term)
async def get_term_by_id(tid:int, db: Session = Depends(get_db)):
    terms = term_db.get_term_by_id(db, tid)
    if not terms:
        print("System log: No terms found")
        return []
    return terms