from app.db.session import engine, SessionLocal
from sqlalchemy import text

url = engine.url.render_as_string(hide_password=True)
with engine.connect() as conn:
    users = conn.execute(text("SELECT COUNT(*) FROM users")).scalar_one()
print("DB:", url)
print("Users:", users)
