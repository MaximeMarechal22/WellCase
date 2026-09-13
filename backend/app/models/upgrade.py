from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class Upgrade(Base):
    __tablename__ = "upgrades"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    target_item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    success_chance = Column(Float, nullable=False)  # Percentage chance of success
    was_successful = Column(Boolean, nullable=False)
    virtual_balance_before = Column(Float, nullable=False)
    virtual_balance_after = Column(Float, nullable=False)
    upgraded_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    original_item = relationship("Item", foreign_keys=[original_item_id])
    target_item = relationship("Item", foreign_keys=[target_item_id])