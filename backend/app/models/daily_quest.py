from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from ..db.base import Base

class DailyQuestClaim(Base):
    __tablename__ = "daily_quest_claims"
    __table_args__ = (UniqueConstraint("user_id", "quest_key", "date_key", name="uq_daily_quest_claim"),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    quest_key = Column(String(50), nullable=False)
    date_key = Column(String(10), nullable=False, index=True)
    xp_reward = Column(Integer, nullable=False, default=100)
    claimed_at = Column(DateTime(timezone=True), server_default=func.now())
