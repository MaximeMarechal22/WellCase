from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..db.session import SessionLocal
from ..models import case, case_item, user
from ..schemas import case as case_schema
from ..drop_rates import weighted_relations
from ..condition_service import condition_distribution
from ..core.security import get_current_active_user

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
    """Expose case items with the exact server-side probabilities used for rolls."""
    items = []
    weighted = weighted_relations(
        [relation for relation in db_case.case_items if relation.item],
        float(db_case.price),
    )
    total_weight = sum(weight for _, weight in weighted) or 1.0
    for relation, weight in weighted:
        item = relation.item
        if not item.is_active:
            continue
        items.append({
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "weapon_class": item.weapon_class,
            "rarity": item.rarity,
            "virtual_value": item.virtual_value,
            "image_url": item.image_url,
            "float_value": item.float_value,
            "color": item.color,
            "probability": weight / total_weight * 100.0,
        })
    quality = condition_distribution(float(db_case.price))
    for item in items:
        item["quality_chances"] = [
            {
                "name": row["name"],
                "key": row["key"],
                "probability": round(float(item["probability"]) * float(row["probability"]) / 100.0, 4),
                "condition_multiplier": row["multiplier"],
                "multiplier": row["multiplier"],
            }
            for row in quality
        ]
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
        "quality_chances": quality,
        "items": items,
    }


@router.get("/", response_model=List[case_schema.CaseWithItems])
async def read_cases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    # Always reconcile the catalog before reading it. This repairs a remote DB
    # that already has the original cases but is missing newer cases/relations.
    try:
        from ..catalog_sync import sync_catalog
        sync_catalog(db)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Catalogue indisponible: {exc}") from exc

    rows = (
        db.query(case.Case)
        .options(joinedload(case.Case.case_items).joinedload(case_item.CaseItem.item))
        .filter(case.Case.is_active.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [_serialize_case(row) for row in rows]


@router.get("/preview/{case_id}", response_model=case_schema.CaseWithItems)
async def preview_case(
    case_id: int,
    db: Session = Depends(get_db),
):
    # Keep direct preview links consistent with GET /cases/: repair/sync the
    # catalog before looking up the requested case.
    try:
        from ..catalog_sync import sync_catalog
        sync_catalog(db)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Catalogue indisponible: {exc}") from exc

    db_case = (
        db.query(case.Case)
        .options(joinedload(case.Case.case_items).joinedload(case_item.CaseItem.item))
        .filter(case.Case.id == case_id, case.Case.is_active.is_(True))
        .first()
    )
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    payload = _serialize_case(db_case)
    quality = condition_distribution(float(db_case.price))
    for item in payload.get("items", []):
        item["quality_chances"] = [
            {
                "name": row["name"],
                "key": row["key"],
                "probability": round(float(item["probability"]) * float(row["probability"]) / 100.0, 4),
                "condition_multiplier": row["multiplier"],
                "multiplier": row["multiplier"],
            }
            for row in quality
        ]
    payload["quality_chances"] = quality
    payload["items"] = sorted(payload.get("items", []), key=lambda item: float(item.get("probability") or 0), reverse=True)
    return payload

@router.get("/{case_id}", response_model=case_schema.CaseWithItems)
async def read_case(
    case_id: int,
    db: Session = Depends(get_db),
):
    # Direct case pages must see the same repaired catalogue and drop weights as the list/preview endpoints.
    try:
        from ..catalog_sync import sync_catalog
        sync_catalog(db)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Catalogue indisponible: {exc}") from exc

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
