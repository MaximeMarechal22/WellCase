from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func
from ..db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    virtual_balance = Column(Float, default=10000.0)  # Starting virtual balance in €
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    avatar_url = Column(Text, nullable=True)
    xp = Column(Integer, default=0, nullable=False)
    open3_tokens = Column(Integer, default=0, nullable=False)
    open5_tokens = Column(Integer, default=0, nullable=False)
    lifetime_xp = Column(Integer, default=0, nullable=False)
    prestige_level = Column(Integer, default=0, nullable=False)
    name_color = Column(String(30), default="white", nullable=False)
    cosmetic_badge = Column(String(50), nullable=True)
    cosmetic_theme = Column(String(50), default="default", nullable=False)
