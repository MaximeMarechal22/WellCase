from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class CaseOpening(Base):
    __tablename__ = "case_openings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    virtual_balance_before = Column(Float, nullable=False)
    virtual_balance_after = Column(Float, nullable=False)
    opened_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    case = relationship("Case")
    item = relationship("Item")