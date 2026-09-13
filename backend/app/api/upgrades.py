import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..db.session import SessionLocal
from ..models import inventory, item, upgrade, user
from ..progression_service import award_xp
from ..schemas import upgrade as upgrade_schema
from ..condition_service import effective_value

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def calculate_success_chance(original_value: float, target_value: float, upgrade_level: int = 0) -> float:
    if original_value <= 0 or target_value <= 0 or target_value <= original_value:
        return 0.0
    base = min(95.0, max(1.0, (original_value / target_value) * 100.0))
    level = max(0, int(upgrade_level or 0))
    # Each successful improvement makes the next attempt harder.
    # A 15% relative reduction is applied per previous successful improvement.
    penalty = 0.85 ** level
    return max(0.5, min(95.0, base * penalty))


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

    owned_query = db.query(inventory.Inventory).filter(
        inventory.Inventory.user_id == current_user.id,
        inventory.Inventory.item_id == source.id,
        inventory.Inventory.quantity >= 1,
    )
    if upgrade_data.inventory_id is not None:
        owned_query = owned_query.filter(inventory.Inventory.id == upgrade_data.inventory_id)
    owned = owned_query.order_by(inventory.Inventory.upgrade_level.desc(), inventory.Inventory.id.asc()).first()
    if not owned or owned.quantity < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You do not own this item.")

    db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    source_level = int(getattr(owned, 'upgrade_level', 0) or 0)
    source_effective_value = effective_value(source.virtual_value, owned.condition)
    chance = calculate_success_chance(source_effective_value, float(target.virtual_value), source_level)
    if chance <= 0:
        raise HTTPException(status_code=400, detail="Cette cible n'est pas éligible pour un upgrade.")
    roll = random.uniform(0.0, 100.0)
    success = roll <= chance

    # The server is the single source of truth for the visual result too.
    # The client must never invent an angle that can contradict was_successful.
    green_degrees = max(3.6, min(342.0, float(chance) * 3.6))
    if success:
        # Land safely inside the visible green sector.
        inner_start = min(8.0, green_degrees * 0.18)
        inner_end = max(inner_start + 1.0, green_degrees - min(8.0, green_degrees * 0.18))
        landing_angle = random.uniform(inner_start, inner_end)
    else:
        # Land safely outside the green sector, with a generous visual margin.
        outside_start = min(352.0, green_degrees + 14.0)
        outside_end = 360.0 - 8.0
        if outside_start >= outside_end:
            outside_start = max(green_degrees + 2.0, 1.0)
            outside_end = max(outside_start + 1.0, 359.0)
        landing_angle = random.uniform(outside_start, outside_end)

    balance_before = float(db_user.virtual_balance)

    try:
        owned.quantity -= 1
        if owned.quantity <= 0:
            db.delete(owned)

        if success:
            # The condition follows the upgraded item. If the target already exists
            # in the same condition, keep the strongest upgrade history.
            target_row = (
                db.query(inventory.Inventory)
                .filter(
                    inventory.Inventory.user_id == db_user.id,
                    inventory.Inventory.item_id == target.id,
                    inventory.Inventory.condition == owned.condition,
                )
                .first()
            )
            next_level = source_level + 1
            if target_row:
                target_row.quantity += 1
                target_row.upgrade_level = max(int(target_row.upgrade_level or 0), next_level)
            else:
                db.add(inventory.Inventory(
                    user_id=db_user.id,
                    item_id=target.id,
                    quantity=1,
                    upgrade_level=next_level,
                    condition=owned.condition,
                ))

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
        prestige = int(getattr(db_user, 'prestige_level', 0) or 0)
        award_xp(db_user, int(round(50 * (1 + 0.05 * prestige))))
        record.virtual_balance_after = float(db_user.virtual_balance)
        db.commit()
        db.refresh(record)
        # Transient presentation value: intentionally not persisted in the DB.
        record.landing_angle = landing_angle
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"The upgrade could not be completed: {exc}")

    return record
