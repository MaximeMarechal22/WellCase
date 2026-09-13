from app.db.session import SQLALCHEMY_DATABASE_URL, engine
from sqlalchemy import text

url = SQLALCHEMY_DATABASE_URL
safe = url
if "@" in safe and "://" in safe:
    prefix, tail = safe.split("@", 1)
    if "://" in prefix and ":" in prefix.split("://",1)[1]:
        scheme, creds = prefix.split("://", 1)
        user = creds.split(":", 1)[0]
        safe = f"{scheme}://{user}:***@{tail}"
print("Database:", safe)
with engine.connect() as conn:
    users = conn.execute(text("SELECT COUNT(*) FROM users")).scalar_one()
print("Users:", users)
