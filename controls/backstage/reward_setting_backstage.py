from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import modules.reward_setting_crud as reward_setting_db
import modules.dbConnect as db_connect
from datetime import date
from controls.tools import verify_token, adminAutorizationCheck

router = APIRouter()
get_db = db_connect.get_db


# 定義 Pydantic 模型
class RewardCreate(BaseModel):
    name: str


class RewardUpdate(BaseModel):
    description: str | None
    reward_type: str | None
    reward: int = 0


# 取得獎勵清單
@router.get("/reward_setting")
async def create_reward(
    token_data: dict = Depends(verify_token), db: Session = Depends(get_db)
):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    reward_list = reward_setting_db.get_all_rewards(db)
    if not reward_list:
        raise HTTPException(status_code=500, detail="Reward get failed")
    return reward_list


# 新建獎勵
@router.post("/reward_setting")
async def create_reward(
    reward: RewardCreate,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    reward_check = reward_setting_db.get_reward_by_name(db, reward.name)

    if not reward_check:
        if reward.name == "new user":
            description = "新進會員的獎勵"
            reward_type = "fixed"

        elif reward.name == "order back":
            description = "每一筆訂單都會返回優惠價比例的善泰幣"
            reward_type = "ratio"
            
        else:
            raise HTTPException(status_code=500, detail="Invaild Call")

        created_reward = reward_setting_db.create_reward(
            db,
            name=reward.name,
            description=description,
            reward_type=reward_type,
            reward=0,
        )
        if not created_reward:
            raise HTTPException(status_code=500, detail="Reward creation failed")
        return created_reward
    else:
        raise HTTPException(status_code=500, detail="Already Exist")


# 更新獎勵內容
@router.patch("/reward_setting/{reward_name}")
async def update_reward(
    reward_name: str,
    reward: RewardUpdate,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    # 確認是否為管理員
    adminAutorizationCheck(token_data.get("isAdmin"))

    if (reward_name == "new user" and reward.reward_type == "ratio") or (
        reward.reward_type != "ratio" and reward.reward_type != "fixed"
    ):
        raise HTTPException(status_code=400, detail="Invaild type")

    update_data = reward.dict(exclude_unset=True)  # 排除未設置的字段
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    updated_user = reward_setting_db.update_reward(
        db, reward_name=reward_name, updates=update_data
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
