from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from ..db.session import SessionLocal
from ..models import inventory, item, user
from ..schemas import inventory as inventory_schema
from ..core.security import get_current_active_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[inventory_schema.InventoryWithItem])
async def read_inventory(
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Load inventory items with the related item using joinedload
    inventory_items = db.query(inventory.Inventory).options(
        joinedload(inventory.Inventory.item)
    ).filter(
        inventory.Inventory.user_id == current_user.id
    ).all()
    return inventory_items

@router.post("/", response_model=inventory_schema.Inventory)
async def add_to_inventory(
    inventory_data: inventory_schema.InventoryCreate,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if item exists
    db_item = db.query(item.Item).filter(
        item.Item.id == inventory_data.item_id,
        item.Item.is_active == True
    ).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Check if user already has this item
    db_inventory = db.query(inventory.Inventory).filter(
        inventory.Inventory.user_id == current_user.id,
        inventory.Inventory.item_id == inventory_data.item_id
    ).first()

    if db_inventory:
        # Increase quantity
        db_inventory.quantity += inventory_data.quantity
    else:
        # Create new inventory entry
        db_inventory = inventory.Inventory(
            user_id=current_user.id,
            item_id=inventory_data.item_id,
            quantity=inventory_data.quantity
        )
        db.add(db_inventory)

    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.post("/{inventory_id}/sell")
async def sell_inventory_item(
    inventory_id: int,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Sell exactly one owned item for 75% of its virtual value."""
    db_inventory = (
        db.query(inventory.Inventory)
        .options(joinedload(inventory.Inventory.item))
        .filter(
            inventory.Inventory.id == inventory_id,
            inventory.Inventory.user_id == current_user.id,
        )
        .first()
    )
    if not db_inventory or not db_inventory.item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    if db_inventory.quantity < 1:
        raise HTTPException(status_code=400, detail="This item is no longer available")

    sold_item_id = db_inventory.item_id
    sold_item_name = db_inventory.item.name
    item_value = float(db_inventory.item.virtual_value or 0)
    sell_amount = round(item_value * 0.75, 2)
    balance_before = float(current_user.virtual_balance)

    try:
        db_inventory.quantity -= 1
        if db_inventory.quantity <= 0:
            db.delete(db_inventory)
        current_user.virtual_balance = balance_before + sell_amount
        db.commit()
        db.refresh(current_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="The item could not be sold.")

    return {
        "message": "Item sold",
        "inventory_id": inventory_id,
        "item_id": sold_item_id,
        "item_name": sold_item_name,
        "item_value": item_value,
        "sell_rate": 75.0,
        "amount": sell_amount,
        "balance_before": balance_before,
        "balance_after": float(current_user.virtual_balance),
    }


@router.delete("/{inventory_id}")
async def remove_from_inventory(
    inventory_id: int,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_inventory = db.query(inventory.Inventory).filter(
        inventory.Inventory.id == inventory_id,
        inventory.Inventory.user_id == current_user.id
    ).first()

    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory item not found")

    db.delete(db_inventory)
    db.commit()
    return {"message": "Item removed from inventory"}