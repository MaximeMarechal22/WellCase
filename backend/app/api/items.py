from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..db.session import SessionLocal
from ..models import item, user
from ..schemas import item as item_schema

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/category/{category}", response_model=List[item_schema.Item])
async def read_items_by_category(
    category: str,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(item.Item)
        .filter(item.Item.category == category, item.Item.is_active.is_(True))
        .all()
    )


@router.get("/rarity/{rarity}", response_model=List[item_schema.Item])
async def read_items_by_rarity(
    rarity: str,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(item.Item)
        .filter(item.Item.rarity == rarity, item.Item.is_active.is_(True))
        .all()
    )


@router.get("/", response_model=List[item_schema.Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(item.Item)
        .filter(item.Item.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{item_id}", response_model=item_schema.Item)
async def read_item(
    item_id: int,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_item = (
        db.query(item.Item)
        .filter(item.Item.id == item_id, item.Item.is_active.is_(True))
        .first()
    )
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post("/", response_model=item_schema.Item)
async def create_item(
    item_data: item_schema.ItemCreate,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_item = item.Item(**item_data.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
