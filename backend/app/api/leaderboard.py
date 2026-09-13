import os
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.session import SessionLocal
from ..models import user, case_opening, upgrade, daily_reward

router = APIRouter()
DEFAULT_RESET_AT = "2026-09-13T01:21:40+00:00"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_cutoff():
    raw = os.getenv("LEADERBOARD_RESET_AT", DEFAULT_RESET_AT)
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.fromisoformat(DEFAULT_RESET_AT)


def level_from_xp(xp: int) -> int:
    return max(1, int((xp / 100) ** 0.5) + 1)


def normalized(dt):
    if dt is None:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


@router.get("/")
async def get_leaderboard(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(3, min(int(limit), 100))
    cutoff = reset_cutoff()

    opening_stats = {}
    for row in db.query(case_opening.CaseOpening.user_id, case_opening.CaseOpening.opened_at).all():
        dt = normalized(row[1])
        if dt and dt >= cutoff:
            opening_stats[row[0]] = opening_stats.get(row[0], 0) + 1

    upgrade_stats = {}
    for row in db.query(upgrade.Upgrade.user_id, upgrade.Upgrade.was_successful, upgrade.Upgrade.upgraded_at).all():
        dt = normalized(row[2])
        if not dt or dt < cutoff:
            continue
        stats = upgrade_stats.setdefault(row[0], {"count": 0, "successes": 0})
        stats["count"] += 1
        stats["successes"] += 1 if row[1] else 0

    reward_stats = {}
    for row in db.query(daily_reward.DailyReward.user_id, daily_reward.DailyReward.claimed_at).all():
        dt = normalized(row[1])
        if dt and dt >= cutoff:
            reward_stats[row[0]] = reward_stats.get(row[0], 0) + 1

    rows = []
    for db_user in db.query(user.User).filter(user.User.is_active.is_(True)).all():
        openings = int(opening_stats.get(db_user.id, 0))
        upgrades = upgrade_stats.get(db_user.id, {"count": 0, "successes": 0})
        rewards = int(reward_stats.get(db_user.id, 0))
        xp = openings * 100 + upgrades["count"] * 50 + upgrades["successes"] * 100 + rewards * 25
        if xp <= 0:
            continue
        rows.append({
            "userId": db_user.id,
            "username": db_user.username,
            "avatar_url": db_user.avatar_url,
            "name_color": db_user.name_color,
            "cosmetic_badge": db_user.cosmetic_badge,
            "prestige_level": int(db_user.prestige_level or 0),
            "xp": int(xp),
            "level": level_from_xp(int(xp)),
            "casesOpened": openings,
            "upgrades": int(upgrades["count"]),
            "successfulUpgrades": int(upgrades["successes"]),
            "dailyRewards": rewards,
        })

    rows.sort(key=lambda row: (row["xp"], row["casesOpened"], row["upgrades"]), reverse=True)
    for index, row in enumerate(rows[:limit], start=1):
        row["rank"] = index
    return rows[:limit]
