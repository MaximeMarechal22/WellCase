from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List
from ..db.session import SessionLocal
from ..models import user, case, case_opening, item, upgrade, daily_reward
from ..schemas import user as user_schema
from ..core.security import get_current_active_user, get_admin_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/balance")
async def get_balance(current_user: user.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return {"balance": float(current_user.virtual_balance)}

@router.get("/history")
async def get_history(current_user: user.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Return one consistent, newest-first activity feed for the logged-in user."""
    opening_rows = (
        db.query(case_opening.CaseOpening)
        .options(
            joinedload(case_opening.CaseOpening.case),
            joinedload(case_opening.CaseOpening.item),
        )
        .filter(case_opening.CaseOpening.user_id == current_user.id)
        .all()
    )

    upgrade_rows = (
        db.query(upgrade.Upgrade)
        .options(
            joinedload(upgrade.Upgrade.original_item),
            joinedload(upgrade.Upgrade.target_item),
        )
        .filter(upgrade.Upgrade.user_id == current_user.id)
        .all()
    )

    reward_rows = (
        db.query(daily_reward.DailyReward)
        .filter(daily_reward.DailyReward.user_id == current_user.id)
        .all()
    )

    events = []

    for opening in opening_rows:
        events.append({
            "id": f"opening-{opening.id}",
            "timestamp": opening.opened_at,
            "type": "opening",
            "caseId": opening.case_id,
            "caseName": opening.case.name if opening.case else "Unknown case",
            "caseImageUrl": opening.case.image_url if opening.case else None,
            "itemId": opening.item_id,
            "itemName": opening.item.name if opening.item else "Unknown item",
            "itemImageUrl": opening.item.image_url if opening.item else None,
            "itemRarity": opening.item.rarity if opening.item else None,
            "itemValue": float(opening.item.virtual_value) if opening.item else 0,
            "balanceBefore": float(opening.virtual_balance_before),
            "balanceAfter": float(opening.virtual_balance_after),
        })

    for upgrade_row in upgrade_rows:
        events.append({
            "id": f"upgrade-{upgrade_row.id}",
            "timestamp": upgrade_row.upgraded_at,
            "type": "upgrade",
            "originalItemId": upgrade_row.original_item_id,
            "originalName": upgrade_row.original_item.name if upgrade_row.original_item else "Unknown item",
            "originalImageUrl": upgrade_row.original_item.image_url if upgrade_row.original_item else None,
            "targetItemId": upgrade_row.target_item_id,
            "targetName": upgrade_row.target_item.name if upgrade_row.target_item else "Unknown item",
            "targetImageUrl": upgrade_row.target_item.image_url if upgrade_row.target_item else None,
            "targetValue": float(upgrade_row.target_item.virtual_value) if upgrade_row.target_item else 0,
            "successChance": float(upgrade_row.success_chance),
            "wasSuccessful": bool(upgrade_row.was_successful),
            "balanceBefore": float(upgrade_row.virtual_balance_before),
            "balanceAfter": float(upgrade_row.virtual_balance_after),
        })

    # DailyReward historically did not store before/after balances. Keep the event useful
    # without inventing values; the UI renders a neutral balance marker for rewards.
    for reward_row in reward_rows:
        events.append({
            "id": f"reward-{reward_row.id}",
            "timestamp": reward_row.claimed_at,
            "type": "reward",
            "dayStreak": reward_row.day_streak,
            "rewardAmount": float(reward_row.reward_amount),
            "balanceBefore": None,
            "balanceAfter": None,
        })

    events.sort(key=lambda event: event["timestamp"] or 0, reverse=True)
    return events
