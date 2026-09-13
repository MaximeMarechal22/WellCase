from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from .item import Item

class MarketListingCreate(BaseModel):
    inventory_id: int
    price: float = Field(gt=0, le=100000000)

class MarketListing(BaseModel):
    id: int
    seller_id: int
    seller_username: str
    item_id: int
    price: float
    created_at: datetime
    item: Item
    is_mine: bool = False
    model_config = ConfigDict(from_attributes=True)
