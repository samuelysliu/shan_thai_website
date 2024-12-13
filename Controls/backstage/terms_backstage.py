from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import modules.term_crud as term_db
import modules.dbConnect as db_connect
from controls.tools import format_to_utc8 as timeformat
from controls.tools import verify_token, adminAutorizationCheck

router = APIRouter()
get_db = db_connect.get_db

# 條款的 Pydantic 模型
class Term(BaseModel):
    name: str
    content: str
    version: str

    class Config:
        from_attributes = True
        
class ResponseTerm(Term):
    tid: int
    

# 新增條款
@router.post("/terms", response_model=ResponseTerm)
async def create_term(term: Term, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    created_term = term_db.create_term(
        db, name=term.name, content=term.content, version=term.version
    )
    if not created_term:
        raise HTTPException(status_code=500, detail="Failed to create term")
    return created_term

# 獲取所有條款
@router.get("/terms", response_model=list[ResponseTerm])
async def get_all_terms(token_data: dict = Depends(verify_token),db: Session = Depends(get_db)):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    terms = term_db.get_all_terms(db)
    if not terms:
        print("System log: No terms found")
        return []
    return terms

# 更新條款
@router.patch("/terms/{tid}", response_model=ResponseTerm)
async def update_term(
    tid: int, updates: dict, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update")
    updated_term = term_db.update_term(db, tid=tid, updates=updates)
    if not updated_term:
        raise HTTPException(status_code=404, detail="Term not found")
    return updated_term

# 刪除條款
@router.delete("/terms/{tid}")
async def delete_term(tid: int, token_data: dict = Depends(verify_token), db: Session = Depends(get_db)):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))
    
    success = term_db.delete_term(db, tid)
    if not success:
        raise HTTPException(status_code=404, detail="Term not found")
    return {"detail": "Term deleted successfully"}
