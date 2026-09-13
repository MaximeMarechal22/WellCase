from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CaseBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    color: Optional[str] = None
    is_active: bool = True


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    color: Optional[str] = None
    is_active: Optional[bool] = None


class Case(CaseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CaseItemBase(BaseModel):
    item_id: int
    probability: float


class CaseItem(CaseItemBase):
    id: int
    case_id: int

    model_config = ConfigDict(from_attributes=True)


class CaseContentItem(BaseModel):
    id: int
    name: str
    category: str
    weapon_class: Optional[str] = None
    rarity: str
    virtual_value: float
    image_url: Optional[str] = None
    float_value: Optional[float] = None
    color: Optional[str] = None
    probability: float = Field(ge=0)


class CaseWithItems(Case):
    items: List[CaseContentItem] = Field(default_factory=list)
