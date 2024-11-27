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


@router.post("/terms", response_model=Term)
async def create_term(term: Term, db: Session = Depends(get_db)):
    """
    新增條款
    """
    created_term = term_db.create_term(
        db, name=term.name, content=term.content, version=term.version
    )
    if not created_term:
        raise HTTPException(status_code=500, detail="Failed to create term")
    return created_term


@router.get("/terms/{tid}", response_model=Term)
async def get_term(tid: int, db: Session = Depends(get_db)):
    """
    根據 tid 獲取條款
    """
    term = term_db.get_term_by_id(db, tid)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term


@router.get("/terms", response_model=list[Term])
async def get_all_terms(db: Session = Depends(get_db)):
    """
    獲取所有條款
    """
    terms = term_db.get_all_terms(db)
    if not terms:
        raise HTTPException(status_code=404, detail="No terms found")
    return terms


@router.patch("/terms/{tid}", response_model=Term)
async def update_term(
    tid: int, updates: dict, db: Session = Depends(get_db)
):
    """
    更新條款
    """
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_term = term_db.update_term(db, tid=tid, updates=updates)
    if not updated_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return updated_term


@router.delete("/terms/{tid}")
async def delete_term(tid: int, db: Session = Depends(get_db)):
    """
    刪除條款
    """
    success = term_db.delete_term(db, tid)
    if not success:
        raise HTTPException(status_code=404, detail="Term not found")
    return {"detail": "Term deleted successfully"}
