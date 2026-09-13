from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1)
    upgrade_level = Column(Integer, default=0, nullable=False)
    condition = Column(String(32), default="État moyen", nullable=False)
    acquired_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship to the Item model
    item = relationship("Item", foreign_keys=[item_id])