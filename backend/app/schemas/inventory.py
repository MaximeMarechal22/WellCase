from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .item import Item

class InventoryBase(BaseModel):
    quantity: int

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