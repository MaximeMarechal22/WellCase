from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models import user
import hashlib
from passlib.context import CryptContext

# Secret key for JWT encoding
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Compatibility layer: existing WellCase accounts may use SHA-256 while older
# databases may contain bcrypt hashes. New accounts continue using SHA-256 for
# backwards compatibility, while bcrypt accounts are transparently migrated
# after a successful login.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    if not hashed_password:
        return False
    # Current WellCase hash format.
    sha256_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    if hashed_password == sha256_hash:
        return True
    # Legacy bcrypt/passlib hashes.
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False
    return False

def get_password_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def is_legacy_bcrypt_hash(hashed_password):
    return isinstance(hashed_password, str) and hashed_password.startswith(("$2a$", "$2b$", "$2y$"))

security = HTTPBearer()

def authenticate_user(db: Session, username: str, password: str):
    normalized_username = (username or "").strip()
    # Prefer an exact username match. Only fall back to case-insensitive lookup
    # when there is exactly one matching account. This avoids Maxime/maxime conflicts.
    db_user = (
        db.query(user.User)
        .filter(user.User.username == normalized_username)
        .first()
    )
    if not db_user:
        matches = (
            db.query(user.User)
            .filter(user.User.username.ilike(normalized_username))
            .all()
        )
        if len(matches) != 1:
            return False
        db_user = matches[0]
    if not verify_password(password, db_user.hashed_password):
        return False

    # Migrate an older bcrypt account to the current hash format after a
    # successful login. This preserves existing users without resetting them.
    if is_legacy_bcrypt_hash(db_user.hashed_password):
        db_user.hashed_password = get_password_hash(password)
        db.commit()
        db.refresh(db_user)
    return db_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_user = db.query(user.User).filter(user.User.username == username).first()
    if db_user is None:
        raise credentials_exception
    return db_user

def get_current_active_user(current_user: user.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_admin_user(current_user: user.User = Depends(get_current_active_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user