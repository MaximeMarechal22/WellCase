from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    category: str
    weapon_class: Optional[str] = None
    rarity: str
    virtual_value: float
    image_url: Optional[str] = None
    float_value: Optional[float] = None
    color: Optional[str] = None
    is_active: bool = True

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True