import random

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..db.session import SessionLocal
from ..models import case, case_item, case_opening, inventory, user
from ..progression_service import award_xp, collection_completion

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# Economy tuning: profitable/high-value drops are intentionally less frequent.
# The original probability remains stored in the DB, while this multiplier is
# applied at roll time and when probabilities are displayed to the player.
def economy_weight(base_probability: float, item_value: float, case_price: float) -> float:
    ratio = float(item_value or 0) / max(float(case_price or 1), 1.0)
    if ratio <= 0.75: multiplier = 1.10
    elif ratio <= 1.0: multiplier = 0.95
    elif ratio <= 1.5: multiplier = 0.55
    elif ratio <= 2.0: multiplier = 0.30
    elif ratio <= 4.0: multiplier = 0.12
    else: multiplier = 0.035
    return max(float(base_probability or 0), 0.0) * multiplier


def weighted_relations(relations, case_price):
    valid = [
        relation for relation in relations
        if relation.item and relation.item.is_active and float(relation.probability or 0) > 0
    ]
    return [(relation, economy_weight(relation.probability, relation.item.virtual_value, case_price)) for relation in valid]

def choose_case_item(case_items):
    valid = [
        relation for relation in case_items
        if relation.item and relation.item.is_active and float(relation.probability or 0) > 0
    ]
    if not valid:
        raise HTTPException(status_code=400, detail="This case has no available rewards.")

    # Kept for backwards compatibility; callers that know the case price should
    # use choose_case_item_for_price below.
    return random.choices(valid, weights=[float(relation.probability) for relation in valid], k=1)[0]


def wealth_snapshot(db, user_id, balance):
    from sqlalchemy import func as sqlfunc
    from ..models import inventory as inv_model, item as item_model
    total = db.query(sqlfunc.coalesce(sqlfunc.sum(inv_model.Inventory.quantity * item_model.Item.virtual_value), 0.0)).join(item_model.Item, inv_model.Inventory.item_id == item_model.Item.id).filter(inv_model.Inventory.user_id == user_id).scalar() or 0.0
    return float(total), float(balance) + float(total)

def choose_case_item_for_price(case_items, case_price):
    weighted = weighted_relations(case_items, case_price)
    if not weighted:
        raise HTTPException(status_code=400, detail="This case has no available rewards.")
    return random.choices(
        [relation for relation, _ in weighted],
        weights=[weight for _, weight in weighted],
        k=1,
    )[0]


@router.post("/{case_id}")
async def open_case(
    case_id: int,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_case = (
        db.query(case.Case)
        .filter(case.Case.id == case_id, case.Case.is_active.is_(True))
        .first()
    )
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")

    price = float(db_case.price)
    balance_before = float(db_user.virtual_balance)
    if balance_before < price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. You need {price:,.0f} €.",
        )

    relations = (
        db.query(case_item.CaseItem)
        .filter(case_item.CaseItem.case_id == case_id)
        .all()
    )
    selected = choose_case_item_for_price(relations, price)
    db_item = selected.item
    balance_after = balance_before - price

    try:
        db_opening = case_opening.CaseOpening(
            user_id=db_user.id,
            case_id=db_case.id,
            item_id=db_item.id,
            virtual_balance_before=balance_before,
            virtual_balance_after=balance_after,
        )
        db.add(db_opening)

        db_inventory = (
            db.query(inventory.Inventory)
            .filter(
                inventory.Inventory.user_id == db_user.id,
                inventory.Inventory.item_id == db_item.id,
            )
            .first()
        )
        if db_inventory:
            db_inventory.quantity += 1
        else:
            db.add(inventory.Inventory(user_id=db_user.id, item_id=db_item.id, quantity=1))

        db_user.virtual_balance = balance_after
        xp_gain = int(round(100 * (1 + 0.05 * int(db_user.prestige_level or 0))))
        if collection_completion(db, db_user.id, getattr(db_item, "weapon_class", None)):
            xp_gain += 25
        award_xp(db_user, xp_gain)
        db.commit()
        db.refresh(db_opening)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="The case opening could not be completed.")

    inventory_value_after, total_wealth_after = wealth_snapshot(db, db_user.id, balance_after)
    weighted = weighted_relations(relations, price)
    total_weight = sum(weight for _, weight in weighted)
    selected_weight = next((weight for relation, weight in weighted if relation.id == selected.id), 0)
    displayed_probability = (selected_weight / total_weight * 100) if total_weight else 0

    rewards = [
        {
            "id": relation.item.id,
            "name": relation.item.name,
            "category": relation.item.category,
            "rarity": relation.item.rarity,
            "virtual_value": relation.item.virtual_value,
            "image_url": relation.item.image_url,
            "color": relation.item.color,
            "probability": (weight / total_weight * 100) if total_weight else 0,
        }
        for relation, weight in weighted
    ]

    return {
        "id": db_opening.id,
        "user_id": db_user.id,
        "case_id": db_case.id,
        "item_id": db_item.id,
        "probability": displayed_probability,
        "virtual_balance_before": balance_before,
        "virtual_balance_after": balance_after,
        "opened_at": db_opening.opened_at,
        "case_price": price,
        "case_name": db_case.name,
        "case_image_url": db_case.image_url,
        "item_value": float(db_item.virtual_value),
        "net_gain": float(db_item.virtual_value) - price,
        "resale_value": round(float(db_item.virtual_value) * 0.75, 2),
        "inventory_added": True,
        "inventory_value_after": inventory_value_after,
        "total_wealth_after": total_wealth_after,
        "rewards": rewards,
        "item": {
            "id": db_item.id,
            "name": db_item.name,
            "category": db_item.category,
            "weapon_class": db_item.weapon_class,
            "rarity": db_item.rarity,
            "virtual_value": db_item.virtual_value,
            "image_url": db_item.image_url,
            "color": db_item.color,
        },
    }

@router.post("/{case_id}/batch")
async def open_case_batch(
    case_id: int,
    count: int = 3,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if count not in (3, 5):
        raise HTTPException(status_code=400, detail="Batch size must be 3 or 5.")
    db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
    db_case = db.query(case.Case).filter(case.Case.id == case_id, case.Case.is_active.is_(True)).first()
    if not db_user or not db_case:
        raise HTTPException(status_code=404, detail="Case not found.")
    token_field = "open3_tokens" if count == 3 else "open5_tokens"
    tokens = int(getattr(db_user, token_field) or 0)
    if tokens < 1:
        raise HTTPException(status_code=400, detail=f"Il te faut un ticket d'ouverture ×{count}.")
    total_price = float(db_case.price) * count
    if float(db_user.virtual_balance or 0) < total_price:
        raise HTTPException(status_code=400, detail=f"Solde insuffisant : {total_price:,.0f} € nécessaires.")
    relations = db.query(case_item.CaseItem).filter(case_item.CaseItem.case_id == case_id).all()
    results = []
    balance = float(db_user.virtual_balance or 0)
    try:
        setattr(db_user, token_field, tokens - 1)
        for _ in range(count):
            selected = choose_case_item_for_price(relations, float(db_case.price))
            db_item = selected.item
            before = balance
            balance -= float(db_case.price)
            db_opening = case_opening.CaseOpening(user_id=db_user.id, case_id=db_case.id, item_id=db_item.id, virtual_balance_before=before, virtual_balance_after=balance)
            db.add(db_opening)
            owned = db.query(inventory.Inventory).filter(inventory.Inventory.user_id == db_user.id, inventory.Inventory.item_id == db_item.id).first()
            if owned:
                owned.quantity += 1
            else:
                db.add(inventory.Inventory(user_id=db_user.id, item_id=db_item.id, quantity=1))
            weighted = weighted_relations(relations, float(db_case.price))
            total_weight = sum(weight for _, weight in weighted) or 1.0
            selected_weight = next((weight for relation, weight in weighted if relation.id == selected.id), 0)
            rewards = [{"id": r.item.id, "name": r.item.name, "category": r.item.category, "weapon_class": r.item.weapon_class, "rarity": r.item.rarity, "virtual_value": r.item.virtual_value, "image_url": r.item.image_url, "color": r.item.color, "probability": weight / total_weight * 100} for r, weight in weighted]
            results.append({"id": None, "user_id": db_user.id, "case_id": db_case.id, "item_id": db_item.id, "probability": selected_weight / total_weight * 100, "virtual_balance_before": before, "virtual_balance_after": balance, "case_price": float(db_case.price), "case_name": db_case.name, "case_image_url": db_case.image_url, "item_value": float(db_item.virtual_value), "net_gain": float(db_item.virtual_value) - float(db_case.price), "rewards": rewards, "item": {"id": db_item.id, "name": db_item.name, "category": db_item.category, "weapon_class": db_item.weapon_class, "rarity": db_item.rarity, "virtual_value": db_item.virtual_value, "image_url": db_item.image_url, "color": db_item.color}})
        db_user.virtual_balance = balance
        xp_gain = 0
        for batch_item in results:
            xp_gain += int(round(100 * (1 + 0.05 * int(db_user.prestige_level or 0))))
            if collection_completion(db, db_user.id, batch_item["item"].get("weapon_class")):
                xp_gain += 25
        award_xp(db_user, xp_gain)
        db.commit()
        for i, r in enumerate(results):
            # IDs are optional for the animation; refresh records isn't required here.
            pass
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Les ouvertures multiples n'ont pas pu être finalisées.")
    inventory_value_after, total_wealth_after = wealth_snapshot(db, db_user.id, balance)
    for batch_result in results:
        batch_result["inventory_value_after"] = inventory_value_after
        batch_result["total_wealth_after"] = total_wealth_after
    return {"count": count, "balance_after": balance, "inventory_value_after": inventory_value_after, "total_wealth_after": total_wealth_after, "xp": db_user.xp, "open3_tokens": db_user.open3_tokens, "open5_tokens": db_user.open5_tokens, "results": results}
