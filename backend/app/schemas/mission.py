from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class MissionBase(BaseModel):
    mission_type: str
    progress: int = 0
    goal: int
    reward_amount: float
    is_completed: bool = False

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)