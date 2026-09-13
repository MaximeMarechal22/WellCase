"""Seed a fresh WellCase database using DATABASE_URL."""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.models import user, case, item, case_item, case_opening, upgrade, daily_reward, inventory, mission


def seed():
    if not os.getenv("DATABASE_URL"):
        raise SystemExit("DATABASE_URL is required.")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(case.Case).first() or db.query(item.Item).first():
            print("Database already contains cases/items; refusing to duplicate seed data.")
            return

        cases_data = [
            ("Beginner Case", "Perfect for new players", 100.0, "/images/cases/beginner.png", "#3498db"),
            ("Advanced Case", "For experienced players", 500.0, "/images/cases/advanced.png", "#9b59b6"),
            ("Elite Case", "For elite players", 1000.0, "/images/cases/elite.png", "#e74c3c"),
            ("AK Specialist Case", "Specialized for AK skins", 750.0, "/images/cases/ak_specialist.png", "#e67e22"),
            ("AWP Specialist Case", "Specialized for AWP skins", 800.0, "/images/cases/awp_specialist.png", "#f39c12"),
        ]
        db_cases = []
        for name, desc, price, image, color in cases_data:
            row = case.Case(name=name, description=desc, price=price, image_url=image, color=color, is_active=True)
            db.add(row); db_cases.append(row)

        items_data = [
            ("AK-47 | Redline", "AK", "Classified", 350.0, "/images/items/ak_redline.png", 0.15, "#bf0d3e"),
            ("AK-47 | Vulcan", "AK", "Classified", 420.0, "/images/items/ak_vulcan.png", 0.08, "#bf0d3e"),
            ("AK-47 | Fire Serpent", "AK", "Covert", 850.0, "/images/items/ak_fire_serpent.png", 0.12, "#bf0d3e"),
            ("AK-47 | Neon Rider", "AK", "Classified", 280.0, "/images/items/ak_neon_rider.png", 0.05, "#bf0d3e"),
            ("AK-47 | Jaguar", "AK", "Restricted", 180.0, "/images/items/ak_jaguar.png", 0.22, "#bf0d3e"),
            ("M4A4 | Howl", "M4", "Contraband", 1200.0, "/images/items/m4_howl.png", 0.03, "#9b59b6"),
            ("M4A1-S | Hyper Beast", "M4", "Classified", 380.0, "/images/items/m4_hyper_beast.png", 0.11, "#9b59b6"),
            ("M4A4 | Neo-Noir", "M4", "Classified", 290.0, "/images/items/m4_neo_noir.png", 0.07, "#9b59b6"),
            ("M4A1-S | Guardian", "M4", "Restricted", 160.0, "/images/items/m4_guardian.png", 0.18, "#9b59b6"),
            ("AWP | Dragon Lore", "AWP", "Contraband", 2500.0, "/images/items/awp_dragon_lore.png", 0.05, "#e74c3c"),
            ("AWP | Asiimov", "AWP", "Classified", 220.0, "/images/items/awp_asiimov.png", 0.15, "#e74c3c"),
            ("AWP | Medusa", "AWP", "Covert", 950.0, "/images/items/awp_medusa.png", 0.09, "#e74c3c"),
            ("AWP | Lightning Strike", "AWP", "Classified", 180.0, "/images/items/awp_lightning_strike.png", 0.12, "#e74c3c"),
            ("Desert Eagle | Blaze", "Desert Eagle", "Classified", 210.0, "/images/items/deagle_blaze.png", 0.14, "#e67e22"),
            ("Desert Eagle | Crimson Web", "Desert Eagle", "Restricted", 85.0, "/images/items/deagle_crimson_web.png", 0.08, "#e67e22"),
            ("Glock-18 | Fade", "Glock", "Classified", 190.0, "/images/items/glock_fade.png", 0.06, "#e67e22"),
            ("USP-S | Kill Confirmed", "USP", "Classified", 150.0, "/images/items/usp_kill_confirmed.png", 0.11, "#e67e22"),
            ("Karambit | Fade", "knife", "Covert", 1800.0, "/images/items/karambit_fade.png", 0.18, "#9b59b6"),
            ("M9 Bayonet | Crimson Web", "knife", "Covert", 850.0, "/images/items/m9_crimson_web.png", 0.22, "#9b59b6"),
            ("Butterfly Knife | Doppler", "knife", "Covert", 1200.0, "/images/items/butterfly_doppler.png", 0.15, "#9b59b6"),
            ("Sport Gloves | Pandora's Box", "gloves", "Extraordinary", 320.0, "/images/items/sport_pandora.png", 0.18, "#f39c12"),
            ("Driver Gloves | Imperial Plaid", "gloves", "Extraordinary", 280.0, "/images/items/driver_imperial.png", 0.15, "#f39c12"),
        ]
        db_items=[]
        for name, category, rarity, value, image, flt, color in items_data:
            row=item.Item(name=name, category=category, rarity=rarity, virtual_value=value, image_url=image, float_value=flt, color=color, is_active=True)
            db.add(row); db_items.append(row)
        db.flush()

        mappings = [
            (0, [(4,35),(7,30),(14,20),(16,10),(0,5)]),
            (1, [(0,25),(1,20),(6,20),(7,15),(10,10),(15,10)]),
            (2, [(2,15),(9,12),(13,10),(17,8),(18,5)]),
            (3, [(0,30),(1,25),(2,20),(3,15),(4,10)]),
            (4, [(9,35),(10,25),(11,20),(12,15),(13,5)]),
        ]
        for case_index, pairs in mappings:
            for item_index, probability in pairs:
                db.add(case_item.CaseItem(case_id=db_cases[case_index].id, item_id=db_items[item_index].id, probability=probability))

        db.commit()
        print("WellCase production database seeded.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
