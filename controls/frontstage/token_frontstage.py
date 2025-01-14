from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import modules.shan_thai_token_crud as token_db
import modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db

# 根據用戶 ID 獲取紅利記錄
@router.get("/tokens/{uid}")
async def get_token(uid: int, db: Session = Depends(get_db)):
    token = token_db.get_token_by_uid(db, uid)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token