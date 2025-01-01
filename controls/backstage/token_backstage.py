from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import modules.shan_thai_token_crud as token_db
import modules.dbConnect as db_connect

router = APIRouter()
get_db = db_connect.get_db


# 定義 Pydantic 模型
class TokenCreate(BaseModel):
    uid: int
    initial_balance: int = 0


class TokenUpdate(BaseModel):
    balance: int

# 根據用戶 ID 獲取紅利記錄
@router.get("/tokens/{uid}")
async def get_token(uid: int, db: Session = Depends(get_db)):
    token = token_db.get_token_by_uid(db, uid)
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    return token


# 更新紅利記錄
@router.post("/tokens/{uid}")
async def upsert_token(uid: int, token_request: TokenUpdate, db: Session = Depends(get_db)):
    """
    創建或更新紅利記錄。如果用戶沒有紅利記錄，則創建；否則更新餘額。
    """
    try:
        # 檢查是否存在紅利記錄
        token = token_db.get_token_by_uid(db, uid)
        if token:
            # 更新紅利餘額
            if token_request.balance < 0:
                raise HTTPException(status_code=400, detail="Balance cannot be negative")
            updated_token = token_db.update_token_balance(db, uid=uid, new_balance=token_request.balance)
            return updated_token
        else:
            # 創建紅利記錄
            new_token = token_db.create_token(db, uid=uid, initial_balance=token_request.balance)
            return new_token
    except:
        raise HTTPException(status_code=500, detail="Failed to upsert token")