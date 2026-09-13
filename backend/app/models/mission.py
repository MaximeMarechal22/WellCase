from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    mission_type = Column(String(50), nullable=False)  # e.g., "open_3_cases", "perform_upgrade"
    progress = Column(Integer, default=0)  # Current progress toward goal
    goal = Column(Integer, nullable=False)  # Target number to complete mission
    reward_amount = Column(Float, nullable=False)  # Reward in virtual €
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User")