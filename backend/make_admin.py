"""Promote an existing WellCase user to admin.

Usage:
    python make_admin.py USERNAME

For Vercel/production, prefer setting ADMIN_USERNAME in the environment
and redeploying/restarting once the user exists.
"""
import sys
from app.db.session import SessionLocal
from app.models.user import User

def main():
    if len(sys.argv) != 2:
        print("Usage: python make_admin.py USERNAME")
        raise SystemExit(2)
    username = sys.argv[1].strip()
    db = SessionLocal()
    try:
        target = db.query(User).filter(User.username == username).first()
        if not target:
            print(f"User not found: {username}")
            raise SystemExit(1)
        target.is_admin = True
        db.commit()
        print(f"OK: {target.username} is now admin.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
