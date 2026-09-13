import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..db.session import SessionLocal
from ..models import inventory, item, upgrade, user
from ..progression_service import award_xp
from ..schemas import upgrade as upgrade_schema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calculate_success_chance(original_value: float, target_value: float) -> float:
    if original_value <= 0 or target_value <= 0 or target_value <= original_value:
        return 0.0
    return min(95.0, max(1.0, (original_value / target_value) * 100.0))


@router.post("/", response_model=upgrade_schema.Upgrade)
async def perform_upgrade(
    upgrade_data: upgrade_schema.UpgradeCreate,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if upgrade_data.original_item_id == upgrade_data.target_item_id:
        raise HTTPException(status_code=400, detail="Choose a different target item.")

    source = (
        db.query(item.Item)
        .filter(item.Item.id == upgrade_data.original_item_id, item.Item.is_active.is_(True))
        .first()
    )
    target = (
        db.query(item.Item)
        .filter(item.Item.id == upgrade_data.target_item_id, item.Item.is_active.is_(True))
        .first()
    )
    if not source or not target:
        raise HTTPException(status_code=404, detail="Item not found.")

    if float(target.virtual_value) <= float(source.virtual_value):
        raise HTTPException(status_code=400, detail="Target must be more valuable than the source item.")

    owned = (
        db.query(inventory.Inventory)
        .filter(
            inventory.Inventory.user_id == current_user.id,
            inventory.Inventory.item_id == source.id,
        )
        .first()
    )
    if not owned or owned.quantity < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You do not own this item.")

    db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    chance = calculate_success_chance(float(source.virtual_value), float(target.virtual_value))
    roll = random.uniform(0.0, 100.0)
    success = roll <= chance
    balance_before = float(db_user.virtual_balance)

    try:
        owned.quantity -= 1
        if owned.quantity <= 0:
            db.delete(owned)

        if success:
            target_owned = (
                db.query(inventory.Inventory)
                .filter(
                    inventory.Inventory.user_id == db_user.id,
                    inventory.Inventory.item_id == target.id,
                )
                .first()
            )
            if target_owned:
                target_owned.quantity += 1
            else:
                db.add(inventory.Inventory(user_id=db_user.id, item_id=target.id, quantity=1))

        record = upgrade.Upgrade(
            user_id=db_user.id,
            original_item_id=source.id,
            target_item_id=target.id,
            success_chance=chance,
            was_successful=success,
            virtual_balance_before=balance_before,
            virtual_balance_after=balance_before,
        )
        db.add(record)
        award_xp(db_user, int(round(50 * (1 + 0.05 * int(db_user.prestige_level or 0)))))
        db.commit()
        db.refresh(record)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="The upgrade could not be completed.")

    return record
