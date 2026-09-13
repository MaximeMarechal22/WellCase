from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class DailyReward(Base):
    __tablename__ = "daily_rewards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    day_streak = Column(Integer, nullable=False)  # Current streak day (1-7)
    reward_amount = Column(Float, nullable=False)  # Reward in virtual €
    claimed_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")