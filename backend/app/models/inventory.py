from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..condition_service import condition_multiplier, effective_value
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

    @property
    def condition_multiplier(self) -> float:
        return condition_multiplier(self.condition)

    @property
    def effective_value(self) -> float:
        base_value = self.item.virtual_value if self.item is not None else 0.0
        return effective_value(base_value, self.condition)
