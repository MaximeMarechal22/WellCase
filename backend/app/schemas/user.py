from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool = True
    is_admin: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    virtual_balance: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    avatar_url: Optional[str] = None
    xp: int = 0
    open3_tokens: int = 0
    open5_tokens: int = 0
    lifetime_xp: int = 0
    prestige_level: int = 0
    name_color: str = "white"
    cosmetic_badge: Optional[str] = None
    cosmetic_theme: str = "default"

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserAvatarUpdate(BaseModel):
    avatar_url: Optional[str] = None
