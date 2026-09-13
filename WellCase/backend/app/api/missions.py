from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ..db.session import SessionLocal
from ..models import mission, case_opening, upgrade, user
from ..schemas import mission as mission_schema
from ..core.security import get_current_active_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[mission_schema.Mission])
async def read_missions(
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    missions = db.query(mission.Mission).filter(
        mission.Mission.user_id == current_user.id
    ).all()
    return missions

@router.post("/check_case_opening")
async def check_case_opening_mission(
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get user from db session to ensure it's tracked by this session
    db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check for "open_3_cases" mission
    mission = db.query(mission.Mission).filter(
        mission.Mission.user_id == db_user.id,
        mission.Mission.mission_type == "open_3_cases",
        mission.Mission.is_completed == False
    ).first()

    if mission:
        # Count user's case openings
        opening_count = db.query(case_opening.CaseOpening).filter(
            case_opening.CaseOpening.user_id == db_user.id
        ).count()

        mission.progress = min(opening_count, mission.goal)
        if mission.progress >= mission.goal:
            mission.is_completed = True
            mission.completed_at = datetime.utcnow()
            # Award reward
            new_balance = current_user.virtual_balance + mission.reward_amount
            db.query(user.User).filter(user.User.id == current_user.id).update(
                {user.User.virtual_balance: new_balance}
            )

        db.commit()

        # Extract values from ORM objects while they're still in the session
        mission_id = mission.id
        mission_progress = mission.progress
        mission_is_completed = mission.is_completed
        mission_completed_at = mission.completed_at

        return {
            "mission": {
                "id": mission_id,
                "user_id": current_user.id,
                "mission_type": mission.mission_type,
                "goal": mission.goal,
                "progress": mission_progress,
                "is_completed": mission_is_completed,
                "completed_at": mission_completed_at,
                "reward_amount": mission.reward_amount
            },
            "message": "Mission progress updated"
        }

    return {"message": "No active case opening mission"}

@router.post("/check_upgrade")
async def check_upgrade_mission(
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check for "perform_upgrade" mission
    mission = db.query(mission.Mission).filter(
        mission.Mission.user_id == current_user.id,
        mission.Mission.mission_type == "perform_upgrade",
        mission.Mission.is_completed == False
    ).first()

    if mission:
        # Get user from db session to ensure it's tracked by this session
        db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Count user's upgrades
        upgrade_count = db.query(upgrade.Upgrade).filter(
            upgrade.Upgrade.user_id == db_user.id
        ).count()

        mission.progress = min(upgrade_count, mission.goal)
        if mission.progress >= mission.goal:
            mission.is_completed = True
            mission.completed_at = datetime.utcnow()
            # Award reward
            new_balance = current_user.virtual_balance + mission.reward_amount
            db.query(user.User).filter(user.User.id == current_user.id).update(
                {user.User.virtual_balance: new_balance}
            )

        db.commit()

        # Extract values from ORM objects while they're still in the session
        mission_id = mission.id
        mission_progress = mission.progress
        mission_is_completed = mission.is_completed
        mission_completed_at = mission.completed_at

        return {
            "mission": {
                "id": mission_id,
                "user_id": current_user.id,
                "mission_type": mission.mission_type,
                "goal": mission.goal,
                "progress": mission_progress,
                "is_completed": mission_is_completed,
                "completed_at": mission_completed_at,
                "reward_amount": mission.reward_amount
            },
            "message": "Mission progress updated"
        }

    return {"message": "No active upgrade mission"}

@router.post("/", response_model=mission_schema.Mission)
async def create_mission(
    mission_data: mission_schema.MissionCreate,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # In a real app, you might have predefined missions or admin-created ones
    db_mission = mission.Mission(
        user_id=current_user.id,
        **mission_data.dict()
    )
    db.add(db_mission)
    db.commit()

    # Extract values from ORM objects while they're still in the session
    mission_id = db_mission.id
    created_at = db_mission.created_at

    # Return response using extracted values
    # This avoids accessing any ORM object attributes after commit
    return {
        "id": mission_id,
        "user_id": current_user.id,
        "mission_type": mission_data.mission_type,
        "goal": mission_data.goal,
        "progress": mission_data.progress,
        "is_completed": mission_data.is_completed,
        "completed_at": created_at,
        "reward_amount": mission_data.reward_amount
    }