from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from ..db.session import get_db
from ..core.security import get_admin_user
from ..models import user, case, case_opening, upgrade, inventory, daily_reward

router = APIRouter()

def _stats(db):
    return {
        "users": db.query(user.User).count(),
        "active_users": db.query(user.User).filter(user.User.is_active == True).count(),
        "admins": db.query(user.User).filter(user.User.is_admin == True).count(),
        "cases": db.query(case.Case).count(),
        "openings": db.query(case_opening.CaseOpening).count(),
        "upgrades": db.query(upgrade.Upgrade).count(),
        "inventory_items": db.query(inventory.Inventory).count(),
        "total_virtual_balance": float(db.query(func.coalesce(func.sum(user.User.virtual_balance), 0)).scalar() or 0),
    }

@router.get("/stats")
def admin_stats(current_user: user.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    return _stats(db)

@router.get("/users")
def admin_users(current_user: user.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    rows = db.query(user.User).order_by(user.User.created_at.desc()).limit(200).all()
    return [{
        "id": u.id, "username": u.username, "email": u.email,
        "balance": float(u.virtual_balance or 0), "is_active": bool(u.is_active),
        "is_admin": bool(u.is_admin), "avatar_url": u.avatar_url,
        "created_at": u.created_at.isoformat() if u.created_at else None,
        "last_login": u.last_login.isoformat() if u.last_login else None,
    } for u in rows]

@router.post("/users/{user_id}/balance")
def admin_balance(user_id: int, payload: dict, current_user: user.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    target = db.query(user.User).filter(user.User.id == user_id).first()
    if not target: raise HTTPException(404, "User not found")
    try: amount = float(payload.get("amount"))
    except (TypeError, ValueError): raise HTTPException(422, "Invalid amount")
    mode = payload.get("mode", "add")
    if mode == "set": target.virtual_balance = max(0, amount)
    else: target.virtual_balance = max(0, float(target.virtual_balance or 0) + amount)
    db.commit()
    return {"user_id": target.id, "balance": float(target.virtual_balance)}

@router.post("/users/{user_id}/status")
def admin_status(user_id: int, payload: dict, current_user: user.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    target = db.query(user.User).filter(user.User.id == user_id).first()
    if not target: raise HTTPException(404, "User not found")
    if target.id == current_user.id and payload.get("is_active") is False:
        raise HTTPException(400, "You cannot disable your own account")
    target.is_active = bool(payload.get("is_active"))
    db.commit()
    return {"user_id": target.id, "is_active": target.is_active}

@router.post("/users/{user_id}/admin")
def admin_role(user_id: int, payload: dict, current_user: user.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    target = db.query(user.User).filter(user.User.id == user_id).first()
    if not target: raise HTTPException(404, "User not found")
    if target.id == current_user.id and payload.get("is_admin") is False:
        raise HTTPException(400, "You cannot remove your own admin role")
    target.is_admin = bool(payload.get("is_admin"))
    db.commit()
    return {"user_id": target.id, "is_admin": target.is_admin}

@router.get("/activity")
def admin_activity(current_user: user.User = Depends(get_admin_user), db: Session = Depends(get_db)):
    openings = db.query(case_opening.CaseOpening).order_by(case_opening.CaseOpening.opened_at.desc()).limit(12).all()
    upgrades = db.query(upgrade.Upgrade).order_by(upgrade.Upgrade.upgraded_at.desc()).limit(12).all()
    return {
        "openings": [{"id": o.id, "user_id": o.user_id, "case_id": o.case_id, "item_id": o.item_id,
                      "date": o.opened_at.isoformat() if o.opened_at else None} for o in openings],
        "upgrades": [{"id": u.id, "user_id": u.user_id, "source_item_id": u.original_item_id,
                      "target_item_id": u.target_item_id, "success": bool(u.was_successful),
                      "date": u.upgraded_at.isoformat() if u.upgraded_at else None} for u in upgrades],
    }
