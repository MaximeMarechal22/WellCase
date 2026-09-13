from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .item import Item

class InventoryBase(BaseModel):
    quantity: int
    upgrade_level: int = 0
    condition: str = "État moyen"
    condition_multiplier: float = 0.65
    effective_value: float = 0.0

class InventoryCreate(InventoryBase):
    item_id: int

class Inventory(InventoryBase):
    id: int
    user_id: int
    item_id: int
    acquired_at: datetime

    class Config:
        from_attributes = True

class InventoryWithItem(Inventory):
    item: Item

    class Config:
        from_attributes = True