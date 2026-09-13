from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DailyRewardBase(BaseModel):
    pass

class DailyRewardCreate(DailyRewardBase):
    pass

class DailyReward(DailyRewardBase):
    id: int
    user_id: int
    day_streak: int
    reward_amount: float
    claimed_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DailyRewardStatus(BaseModel):
    can_claim: bool
    day_streak: Optional[int] = None
    reward_amount: Optional[float] = None
    message: str
    next_available: Optional[datetime] = None