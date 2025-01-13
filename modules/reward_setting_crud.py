from sqlalchemy.orm import Session
from modules.dbInit import RewardSetting
from sqlalchemy.exc import SQLAlchemyError


# 獲取所有獎勵
def get_all_rewards(db: Session):
    try:
        rewards = db.query(RewardSetting).all()
        return [
            {
                "id": reward.id,
                "name": reward.name,
                "description": reward.description,
                "reward_type": reward.reward_type,
                "reward": reward.reward,
                "created_at": reward.created_at,
                "updated_at": reward.updated_at,
            }
            for reward in rewards
        ]
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 根據 name 獲取獎勵
def get_reward_by_name(db: Session, name: str):
    try:
        reward = db.query(RewardSetting).filter(RewardSetting.name == name).first()
        if reward:
            return {
                "id": reward.id,
                "name": reward.name,
                "description": reward.description,
                "reward_type": reward.reward_type,
                "reward": reward.reward,
                "created_at": reward.created_at,
                "updated_at": reward.updated_at,
            }
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 創建新獎勵
def create_reward(
    db: Session,
    name: str,
    description: str = None,
    reward_type: str = None,
    reward: int = 0,
):
    try:
        new_reward = RewardSetting(
            name=name,
            description=description,
            reward_type=reward_type,
            reward=reward,
        )
        db.add(new_reward)
        db.commit()
        db.refresh(new_reward)
        return new_reward
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 更新獎勵
def update_reward(db: Session, reward_id: int, updates: dict):
    try:
        reward = db.query(RewardSetting).filter(RewardSetting.id == reward_id).first()
        if reward:
            for key, value in updates.items():
                if key in {"description", "reward_type", "reward"}:
                    setattr(reward, key, value)
            db.commit()
            db.refresh(reward)
            return reward
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None


# 刪除獎勵
def delete_reward(db: Session, reward_id: int):
    try:
        reward = db.query(RewardSetting).filter(RewardSetting.id == reward_id).first()
        if reward:
            db.delete(reward)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
