import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..db.base import Base

# Load database configuration from all normal project env locations.
# Order: backend/.env, project root/.env, project root/.env.local.
# Existing process environment variables always take precedence because
# load_dotenv(..., override=False) is used.
BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BACKEND_DIR.parent
for env_file in (
    BACKEND_DIR / ".env",
    PROJECT_DIR / ".env",
    PROJECT_DIR / ".env.local",
):
    if env_file.exists():
        load_dotenv(env_file, override=False)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. Put your Neon PostgreSQL connection string in "
        "backend/.env (recommended), project .env/.env.local, or the hosting provider environment."
    )

if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
