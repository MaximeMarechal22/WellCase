from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .item import Item


class UpgradeCreate(BaseModel):
    original_item_id: int
    target_item_id: int


class Upgrade(BaseModel):
    id: int
    user_id: int
    original_item_id: int
    target_item_id: int
    success_chance: float
    was_successful: bool
    virtual_balance_before: float
    virtual_balance_after: float
    upgraded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpgradeWithItems(Upgrade):
    original_item: Item
    target_item: Item
