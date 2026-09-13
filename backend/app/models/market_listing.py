from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.base import Base

class MarketListing(Base):
    __tablename__ = 'market_listings'
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False, index=True)
    price = Column(Float, nullable=False)
    condition = Column(String(32), default="État moyen", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    seller = relationship('User')
    item = relationship('Item')
