from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from .item import Item

class CaseOpeningBase(BaseModel):
    pass

class CaseOpeningCreate(CaseOpeningBase):
    case_id: int

class CaseOpening(CaseOpeningBase):
    id: int
    user_id: int
    case_id: int
    item_id: int
    virtual_balance_before: float
    virtual_balance_after: float
    opened_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CaseOpeningWithItem(CaseOpening):
    item: Item