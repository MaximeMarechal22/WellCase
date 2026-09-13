from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base import Base
from .item import Item


class CaseItem(Base):
    __tablename__ = "case_items"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    probability = Column(Float, nullable=False)  # Weight/percentage in the case.

    item = relationship("Item", foreign_keys=[item_id], lazy="joined")
