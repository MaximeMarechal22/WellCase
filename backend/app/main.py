import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from app.db.base import Base
from app.models import user, daily_quest, battle_pass, market_listing, item
from app.db.session import engine
from app.catalog_sync import migrate_compatibility, sync_catalog, migrate_progression_columns
from app.db.session import SessionLocal

app = FastAPI(title="WellCase API", description="Virtual case opening platform API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("FRONTEND_URLS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
        if origin.strip()
    ],
    allow_origin_regex=os.getenv("FRONTEND_ORIGIN_REGEX", r"https://[a-zA-Z0-9-]+\.vercel\.app"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def ensure_tables():
    migrate_compatibility()
    Base.metadata.create_all(bind=engine)
    migrate_progression_columns()
    db = SessionLocal()
    try:
        sync_catalog(db)

        # Optional first-owner bootstrap. Set ADMIN_USERNAME to the exact
        # username you want to promote once the account exists.
        owner_username = os.getenv("ADMIN_USERNAME", "").strip()
        if owner_username:
            from app.models import user as user_model
            owner = db.query(user_model.User).filter(
                user_model.User.username == owner_username
            ).first()
            if owner and not owner.is_admin:
                owner.is_admin = True
                db.commit()
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to WellCase API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test")
async def test_endpoint():
    return {"message": "Test endpoint is working"}

from app.api import auth, cases, items, inventory, openings, upgrades, daily_rewards, missions, dashboard, leaderboard, admin, progression, market, collections

app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(cases.router, prefix="/cases", tags=["cases"])
app.include_router(items.router, prefix="/items", tags=["items"])
app.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
app.include_router(openings.router, prefix="/openings", tags=["case openings"])
app.include_router(upgrades.router, prefix="/upgrades", tags=["upgrades"])
app.include_router(daily_rewards.router, prefix="/daily-rewards", tags=["daily rewards"])
app.include_router(missions.router, prefix="/missions", tags=["missions"])
app.include_router(dashboard.router, prefix="", tags=["dashboard"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(progression.router, prefix="/progression", tags=["progression"])
app.include_router(market.router, prefix="/market", tags=["market"])
app.include_router(collections.router, prefix="/collections", tags=["collections"]) 
