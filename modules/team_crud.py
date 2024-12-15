from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from modules.dbInit import Team as TeamModel

# 取得所有 Team 資料
def get_team(db: Session):
    try:
        return db.query(TeamModel).all()
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 新增 Team 資料
def create_team(db: Session, No: int, name_cn: str, title_cn: str, teamImageUrl: str):
    try:
        new_team_member = TeamModel(
            No=No,
            name_cn=name_cn,
            title_cn=title_cn,
            teamImageUrl=teamImageUrl
        )
        db.add(new_team_member)
        db.commit()
        db.refresh(new_team_member)
        return new_team_member
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 更新 Team 資料
def update_team(db: Session, team_id: int, No: int, name_cn: str, title_cn: str, teamImageUrl: str):
    try:
        team_member = db.query(TeamModel).filter(TeamModel.id == team_id).first()
        if team_member:
            team_member.No = No
            team_member.name_cn = name_cn
            team_member.title_cn = title_cn
            team_member.teamImageUrl = teamImageUrl
            db.commit()
            db.refresh(team_member)
            return team_member
        return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return None

# 刪除 Team 資料
def delete_team(db: Session, team_id: int):
    try:
        team_member = db.query(TeamModel).filter(TeamModel.id == team_id).first()
        if team_member:
            db.delete(team_member)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"Error: {e}")
        return False
