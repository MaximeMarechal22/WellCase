from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time
from ..db.session import SessionLocal
from ..models import daily_reward, user
from ..schemas import daily_reward as daily_reward_schema
from ..core.security import get_current_active_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def today_window():
    today = datetime.utcnow().date()
    start = datetime.combine(today, time.min)
    end = start + timedelta(days=1)
    return today, start, end

# Define daily reward amounts for each day (1-7)
DAILY_REWARD_AMOUNTS = {
    1: 500.0,
    2: 750.0,
    3: 1000.0,
    4: 1500.0,
    5: 2000.0,
    6: 3000.0,
    7: 5000.0
}

@router.get("/", response_model=daily_reward_schema.DailyRewardStatus)
async def get_daily_reward_status(
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get today's date
    today, start_of_day, end_of_day = today_window()

    # Check today's reward using an explicit [start, end) range for SQLite/PostgreSQL compatibility.
    today_reward = db.query(daily_reward.DailyReward).filter(
        daily_reward.DailyReward.user_id == current_user.id,
        daily_reward.DailyReward.claimed_at >= start_of_day,
        daily_reward.DailyReward.claimed_at < end_of_day
    ).first()

    if today_reward:
        # Already claimed today
        return {
            "can_claim": False,
            "message": "You have already claimed today's reward",
            "next_available": datetime.combine(today + timedelta(days=1), time.min)
        }

    # Get the most recent reward to determine streak
    latest_reward = db.query(daily_reward.DailyReward).filter(
        daily_reward.DailyReward.user_id == current_user.id
    ).order_by(daily_reward.DailyReward.claimed_at.desc()).first()

    # Calculate streak
    if latest_reward:
        last_claim_date = latest_reward.claimed_at.date()
        days_diff = (today - last_claim_date).days

        if days_diff == 1:
            # Consecutive day
            streak = latest_reward.day_streak + 1
        elif days_diff == 0:
            # Same day (shouldn't happen due to above check)
            streak = latest_reward.day_streak
        else:
            # Streak broken
            streak = 1
    else:
        # First ever reward
        streak = 1

    # Cap streak at 7 days (then it resets to 1)
    if streak > 7:
        streak = 1

    reward_amount = DAILY_REWARD_AMOUNTS.get(streak, 0)

    return {
        "can_claim": True,
        "day_streak": streak,
        "reward_amount": reward_amount,
        "message": f"Claim your Day {streak} reward of {reward_amount} €"
    }

@router.post("/claim", response_model=daily_reward_schema.DailyReward)
async def claim_daily_reward(
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Get today's date
    today, start_of_day, end_of_day = today_window()

    # Get user from db session to ensure it's tracked by this session
    db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user already claimed today's reward
    today_reward = db.query(daily_reward.DailyReward).filter(
        daily_reward.DailyReward.user_id == db_user.id,
        daily_reward.DailyReward.claimed_at >= start_of_day,
        daily_reward.DailyReward.claimed_at < end_of_day
    ).first()

    if today_reward:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already claimed today's reward"
        )

    # Get the most recent reward to determine streak
    latest_reward = db.query(daily_reward.DailyReward).filter(
        daily_reward.DailyReward.user_id == db_user.id
    ).order_by(daily_reward.DailyReward.claimed_at.desc()).first()

    # Calculate streak
    if latest_reward:
        last_claim_date = latest_reward.claimed_at.date()
        days_diff = (today - last_claim_date).days

        if days_diff == 1:
            # Consecutive day
            streak = latest_reward.day_streak + 1
        elif days_diff == 0:
            # Same day (shouldn't happen due to above check)
            streak = latest_reward.day_streak
        else:
            # Streak broken
            streak = 1
    else:
        # First ever reward
        streak = 1

    # Cap streak at 7 days (then it resets to 1)
    if streak > 7:
        streak = 1

    reward_amount = DAILY_REWARD_AMOUNTS.get(streak, 0)

    # Add reward to user balance using query to avoid modifying the current_user object directly
    new_balance = current_user.virtual_balance + reward_amount
    db.query(user.User).filter(user.User.id == current_user.id).update(
        {user.User.virtual_balance: new_balance, user.User.xp: user.User.xp + 25}
    )

    # Create daily reward record with values we already have
    db_reward = daily_reward.DailyReward(
        user_id=current_user.id,
        day_streak=streak,
        reward_amount=reward_amount
    )
    db.add(db_reward)

    # Commit all changes
    db.commit()

    # Extract values from ORM objects while they're still in the session
    reward_id = db_reward.id
    claimed_at = db_reward.claimed_at

    # Return response using extracted values
    # This avoids accessing any ORM object attributes after commit
    return {
        "id": reward_id,
        "user_id": current_user.id,
        "day_streak": streak,
        "reward_amount": reward_amount,
        "claimed_at": claimed_at
    }