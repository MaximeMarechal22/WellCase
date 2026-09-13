from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..core.security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_password_hash
)
from ..db.session import get_db, SessionLocal
from ..models import user
from ..schemas import user as user_schema

router = APIRouter()

@router.post("/token", response_model=user_schema.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=user_schema.User)
async def read_users_me(current_user: user.User = Depends(get_current_active_user)):
    return current_user

@router.put("/users/me/avatar", response_model=user_schema.User)
async def update_my_avatar(
    avatar_data: user_schema.UserAvatarUpdate,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    value = avatar_data.avatar_url
    if value is not None and len(value) > 2_000_000:
        raise HTTPException(status_code=413, detail="Avatar is too large. Please use a smaller image.")
    db_user = db.query(user.User).filter(user.User.id == current_user.id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.avatar_url = value
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/{user_id}", response_model=user_schema.User)
async def read_user(
    user_id: int,
    current_user: user.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/users/", response_model=user_schema.User)
async def create_user(
    user_data: user_schema.UserCreate,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    db_user = db.query(user.User).filter(user.User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email already exists
    db_email = db.query(user.User).filter(user.User.email == user_data.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    db_user = user.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        virtual_balance=10000.0  # Starting balance
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/admin/users/", response_model=list[user_schema.User])
async def read_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: user.User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(user.User).offset(skip).limit(limit).all()
    return users