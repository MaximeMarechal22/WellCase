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
    mission_obj = db.query(mission.Mission).filter(
        mission.Mission.user_id == db_user.id,
        mission.Mission.mission_type == "open_3_cases",
        mission.Mission.is_completed == False
    ).first()

    if mission_obj:
        # Count user's case openings
        opening_count = db.query(case_opening.CaseOpening).filter(
            case_opening.CaseOpening.user_id == db_user.id
        ).count()

        mission_obj.progress = min(opening_count, mission_obj.goal)
        if mission_obj.progress >= mission_obj.goal:
            mission_obj.is_completed = True
            mission_obj.completed_at = datetime.utcnow()
            # Award reward using query to avoid modifying the current_user object directly
            new_balance = current_user.virtual_balance + mission_obj.reward_amount
            db.query(user.User).filter(user.User.id == current_user.id).update(
                {user.User.virtual_balance: new_balance}
            )

        db.commit()

        # Extract values from ORM objects while they're still in the session
        mission_id = mission_obj.id
        mission_progress = mission_obj.progress
        mission_is_completed = mission_obj.is_completed
        mission_completed_at = mission_obj.completed_at

        return {
            "mission": {
                "id": mission_id,
                "user_id": current_user.id,
                "mission_type": mission_obj.mission_type,
                "goal": mission_obj.goal,
                "progress": mission_progress,
                "is_completed": mission_is_completed,
                "completed_at": mission_completed_at,
                "reward_amount": mission_obj.reward_amount
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
    mission_obj = db.query(mission.Mission).filter(
        mission.Mission.user_id == current_user.id,
        mission.Mission.mission_type == "perform_upgrade",
        mission.Mission.is_completed == False
    ).first()

    if mission_obj:
        # Get user from db session to ensure it's tracked by this session
        db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Count user's upgrades
        upgrade_count = db.query(upgrade.Upgrade).filter(
            upgrade.Upgrade.user_id == db_user.id
        ).count()

        mission_obj.progress = min(upgrade_count, mission_obj.goal)
        if mission_obj.progress >= mission_obj.goal:
            mission_obj.is_completed = True
            mission_obj.completed_at = datetime.utcnow()
            # Award reward using query to avoid modifying the current_user object directly
            new_balance = current_user.virtual_balance + mission_obj.reward_amount
            db.query(user.User).filter(user.User.id == current_user.id).update(
                {user.User.virtual_balance: new_balance}
            )

        db.commit()

        # Extract values from ORM objects while they're still in the session
        mission_id = mission_obj.id
        mission_progress = mission_obj.progress
        mission_is_completed = mission_obj.is_completed
        mission_completed_at = mission_obj.completed_at

        return {
            "mission": {
                "id": mission_id,
                "user_id": current_user.id,
                "mission_type": mission_obj.mission_type,
                "goal": mission_obj.goal,
                "progress": mission_progress,
                "is_completed": mission_is_completed,
                "completed_at": mission_completed_at,
                "reward_amount": mission_obj.reward_amount
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
    db.refresh(db_mission)

    # Extract values from ORM objects while they're still in the session
    # This matches the pattern used in upgrades.py and avoids ORM detachment issues
    mission_id = db_mission.id
    created_at_value = db_mission.created_at
    completed_at_value = db_mission.completed_at
    updated_at_value = db_mission.updated_at

    # Return response using extracted values
    # This ensures all fields are present and avoids accessing ORM object attributes after commit
    return {
        "id": mission_id,
        "user_id": current_user.id,
        "mission_type": mission_data.mission_type,
        "goal": mission_data.goal,
        "progress": mission_data.progress,
        "is_completed": mission_data.is_completed,
        "completed_at": completed_at_value,
        "updated_at": updated_at_value,
        "reward_amount": mission_data.reward_amount,
        "created_at": created_at_value
    }