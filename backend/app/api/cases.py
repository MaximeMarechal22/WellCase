from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..core.security import get_current_active_user
from ..db.session import SessionLocal
from ..models import case, case_item, user
from ..schemas import case as case_schema

router = APIRouter()

def economy_multiplier(item_value, case_price):
    ratio=float(item_value or 0)/max(float(case_price or 1),1.0)
    if ratio<=.75:return 1.10
    if ratio<=1.0:return .95
    if ratio<=1.5:return .55
    if ratio<=2.0:return .30
    if ratio<=4.0:return .12
    return .035



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _serialize_case(db_case: case.Case) -> dict:
    """Expose case_items as a frontend-friendly flat items array."""
    items = []
    valid_relations = [
        relation for relation in db_case.case_items
        if relation.item and relation.item.is_active and float(relation.probability or 0) > 0
    ]
    weights=[float(relation.probability)*economy_multiplier(relation.item.virtual_value,db_case.price) for relation in valid_relations]
    total_weight = sum(weights) or 1.0
    for relation, weight in zip(valid_relations, weights):
        items.append(
            {
                "id": relation.item.id,
                "name": relation.item.name,
                "category": relation.item.category,
                "weapon_class": relation.item.weapon_class,
                "rarity": relation.item.rarity,
                "virtual_value": relation.item.virtual_value,
                "image_url": relation.item.image_url,
                "float_value": relation.item.float_value,
                "color": relation.item.color,
                "probability": weight / total_weight * 100,
            }
        )
    return {
        "id": db_case.id,
        "name": db_case.name,
        "description": db_case.description,
        "price": db_case.price,
        "image_url": db_case.image_url,
        "color": db_case.color,
        "is_active": db_case.is_active,
        "created_at": db_case.created_at,
        "updated_at": db_case.updated_at,
        "items": items,
    }


@router.get("/", response_model=List[case_schema.Case])
async def read_cases(
    skip: int = 0,
    limit: int = 100,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(case.Case)
        .filter(case.Case.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{case_id}", response_model=case_schema.CaseWithItems)
async def read_case(
    case_id: int,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_case = (
        db.query(case.Case)
        .options(joinedload(case.Case.case_items).joinedload(case_item.CaseItem.item))
        .filter(case.Case.id == case_id, case.Case.is_active.is_(True))
        .first()
    )
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return _serialize_case(db_case)


@router.post("/", response_model=case_schema.Case)
async def create_case(
    case_data: case_schema.CaseCreate,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_case = case.Case(**case_data.model_dump())
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
    return db_case


@router.put("/{case_id}", response_model=case_schema.Case)
async def update_case(
    case_id: int,
    case_data: case_schema.CaseUpdate,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_case = db.query(case.Case).filter(case.Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    for key, value in case_data.model_dump(exclude_unset=True).items():
        setattr(db_case, key, value)

    db.commit()
    db.refresh(db_case)
    return db_case


@router.delete("/{case_id}")
async def delete_case(
    case_id: int,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    db_case = db.query(case.Case).filter(case.Case.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    db_case.is_active = False
    db.commit()
    return {"message": "Case deleted successfully"}
