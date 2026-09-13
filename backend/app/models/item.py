from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func
from ..db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # legacy weapon family
    weapon_class = Column(String(50), nullable=True, index=True)  # Assault Rifles, SMGs, Snipers, Pistols, Knives, Gloves
    rarity = Column(String(20), nullable=False)  # Common, Uncommon, Rare, Epic, Legendary, Mythic
    virtual_value = Column(Float, nullable=False)  # Value in virtual €
    image_url = Column(String(255))
    float_value = Column(Float)  # Fictitious float value for skins
    color = Column(String(20))  # Hex color based on rarity
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())