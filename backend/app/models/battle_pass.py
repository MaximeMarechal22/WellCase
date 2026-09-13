from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from ..db.base import Base

class BattlePassClaim(Base):
    __tablename__ = "battle_pass_claims"
    __table_args__ = (UniqueConstraint("user_id", "season", "level", name="uq_battle_pass_claim"),)
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    season = Column(String(50), nullable=False)
    level = Column(Integer, nullable=False)
    claimed_at = Column(DateTime(timezone=True), server_default=func.now())
