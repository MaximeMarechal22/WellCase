from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.models import user, case, item, case_item, inventory, case_opening, upgrade, daily_reward, mission
import hashlib

# Create tables with a new database URL
from app.db.base import Base

# Override the database URL to use a new file
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a new engine pointing to a different database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./caseforge_new.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Simple password hashing for demo (use proper bcrypt in production)
def get_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    db = SessionLocal()

    # Check if we already have users
    if db.query(user.User).first():
        print("Database already initialized")
        return

    # Create admin user
    admin_user = user.User(
        username="admin",
        email="admin@caseforge.com",
        hashed_password=get_password_hash("admin123"),
        virtual_balance=10000.0,
        is_active=True,
        is_admin=True
    )
    db.add(admin_user)

    # Create regular user
    regular_user = user.User(
        username="player1",
        email="player1@caseforge.com",
        hashed_password=get_password_hash("player123"),
        virtual_balance=10000.0,
        is_active=True,
        is_admin=False
    )
    db.add(regular_user)

    db.commit()

    # Create cases
    cases_data = [
        {
            "name": "Beginner Case",
            "description": "Perfect for new players - contains common and uncommon items",
            "price": 100.0,
            "image_url": "/images/cases/beginner.png",
            "color": "#3498db"
        },
        {
            "name": "Advanced Case",
            "description": "For experienced players - contains rare and epic items",
            "price": 500.0,
            "image_url": "/images/cases/advanced.png",
            "color": "#9b59b6"
        },
        {
            "name": "Elite Case",
            "description": "For elite players - contains legendary and mythic items",
            "price": 1000.0,
            "image_url": "/images/cases/elite.png",
            "color": "#e74c3c"
        },
        {
            "name": "AK Specialist Case",
            "description": "Specialized case for AK skins",
            "price": 750.0,
            "image_url": "/images/cases/ak_specialist.png",
            "color": "#e67e22"
        },
        {
            "name": "AWP Specialist Case",
            "description": "Specialized case for AWP skins",
            "price": 800.0,
            "image_url": "/images/cases/awp_specialist.png",
            "color": "#f39c12"
        }
    ]

    db_cases = []
    for case_data in cases_data:
        db_case = case.Case(**case_data)
        db.add(db_case)
        db_cases.append(db_case)

    db.commit()

    # Create items
    items_data = [
        # AK Skins
        {"name": "AK-47 | Redline", "category": "AK", "rarity": "Classified", "virtual_value": 350.0, "image_url": "/images/items/ak_redline.png", "float_value": 0.15, "color": "#bf0d3e"},
        {"name": "AK-47 | Vulcan", "category": "AK", "rarity": "Classified", "virtual_value": 420.0, "image_url": "/images/items/ak_vulcan.png", "float_value": 0.08, "color": "#bf0d3e"},
        {"name": "AK-47 | Fire Serpent", "category": "AK", "rarity": "Covert", "virtual_value": 850.0, "image_url": "/images/items/ak_fire_serpent.png", "float_value": 0.12, "color": "#bf0d3e"},
        {"name": "AK-47 | Neon Rider", "category": "AK", "rarity": "Classified", "virtual_value": 280.0, "image_url": "/images/items/ak_neon_rider.png", "float_value": 0.05, "color": "#bf0d3e"},
        {"name": "AK-47 | Jaguar", "category": "AK", "rarity": "Restricted", "virtual_value": 180.0, "image_url": "/images/items/ak_jaguar.png", "float_value": 0.22, "color": "#bf0d3e"},

        # M4 Skins
        {"name": "M4A4 | Howl", "category": "M4", "rarity": "Contraband", "virtual_value": 1200.0, "image_url": "/images/items/m4_howl.png", "float_value": 0.03, "color": "#9b59b6"},
        {"name": "M4A1-S | Hyper Beast", "category": "M4", "rarity": "Classified", "virtual_value": 380.0, "image_url": "/images/items/m4_hyper_beast.png", "float_value": 0.11, "color": "#9b59b6"},
        {"name": "M4A4 | Neo-Noir", "category": "M4", "rarity": "Classified", "virtual_value": 290.0, "image_url": "/images/items/m4_neo_noir.png", "float_value": 0.07, "color": "#9b59b6"},
        {"name": "M4A1-S | Guardian", "category": "M4", "rarity": "Restricted", "virtual_value": 160.0, "image_url": "/images/items/m4_guardian.png", "float_value": 0.18, "color": "#9b59b6"},

        # AWP Skins
        {"name": "AWP | Dragon Lore", "category": "AWP", "rarity": "Contraband", "virtual_value": 2500.0, "image_url": "/images/items/awp_dragon_lore.png", "float_value": 0.05, "color": "#e74c3c"},
        {"name": "AWP | Asiimov", "category": "AWP", "rarity": "Classified", "virtual_value": 220.0, "image_url": "/images/items/awp_asiimov.png", "float_value": 0.15, "color": "#e74c3c"},
        {"name": "AWP | Medusa", "category": "AWP", "rarity": "Covert", "virtual_value": 950.0, "image_url": "/images/items/awp_medusa.png", "float_value": 0.09, "color": "#e74c3c"},
        {"name": "AWP | Lightning Strike", "category": "AWP", "rarity": "Classified", "virtual_value": 180.0, "image_url": "/images/items/awp_lightning_strike.png", "float_value": 0.12, "color": "#e74c3c"},

        # Pistols
        {"name": "Desert Eagle | Blaze", "category": "Desert Eagle", "rarity": "Classified", "virtual_value": 210.0, "image_url": "/images/items/deagle_blaze.png", "float_value": 0.14, "color": "#e67e22"},
        {"name": "Desert Eagle | Crimson Web", "category": "Desert Eagle", "rarity": "Restricted", "virtual_value": 85.0, "image_url": "/images/items/deagle_crimson_web.png", "float_value": 0.08, "color": "#e67e22"},
        {"name": "Glock-18 | Fade", "category": "Glock", "rarity": "Classified", "virtual_value": 190.0, "image_url": "/images/items/glock_fade.png", "float_value": 0.06, "color": "#e67e22"},
        {"name": "USP-S | Kill Confirmed", "category": "USP", "rarity": "Classified", "virtual_value": 150.0, "image_url": "/images/items/usp_kill_confirmed.png", "float_value": 0.11, "color": "#e67e22"},

        # Knives
        {"name": "Karambit | Fade", "category": "knife", "rarity": "Covert", "virtual_value": 1800.0, "image_url": "/images/items/karambit_fade.png", "float_value": 0.18, "color": "#9b59b6"},
        {"name": "M9 Bayonet | Crimson Web", "category": "knife", "rarity": "Covert", "virtual_value": 850.0, "image_url": "/images/items/m9_crimson_web.png", "float_value": 0.22, "color": "#9b59b6"},
        {"name": "Butterfly Knife | Doppler", "category": "knife", "rarity": "Covert", "virtual_value": 1200.0, "image_url": "/images/items/butterfly_doppler.png", "float_value": 0.15, "color": "#9b59b6"},

        # Gloves
        {"name": "Sport Gloves | Pandora's Box", "category": "gloves", "rarity": "Extraordinary", "virtual_value": 320.0, "image_url": "/images/items/sport_pandora.png", "float_value": 0.18, "color": "#f39c12"},
        {"name": "Driver Gloves | Imperial Plaid", "category": "gloves", "rarity": "Extraordinary", "virtual_value": 280.0, "image_url": "/images/items/driver_imperial.png", "float_value": 0.15, "color": "#f39c12"},
    ]

    db_items = []
    for item_data in items_data:
        db_item = item.Item(**item_data)
        db.add(db_item)
        db_items.append(db_item)

    db.commit()

    # Create case-item relationships with probabilities
    # Beginner Case (100€) - Common and Uncommon items
    beginner_case_items = [
        (db_items[4], 35.0),   # AK-47 | Jaguar
        (db_items[7], 30.0),   # M4A1-S | Guardian
        (db_items[10], 20.0),  # Desert Eagle | Crimson Web
        (db_items[13], 10.0),  # USP-S | Kill Confirmed
        (db_items[0], 5.0),    # AK-47 | Redline (rare)
    ]

    # Advanced Case (500€) - Rare and Epic items
    advanced_case_items = [
        (db_items[0], 25.0),   # AK-47 | Redline
        (db_items[1], 20.0),   # AK-47 | Vulcan
        (db_items[5], 20.0),   # M4A1-S | Hyper Beast
        (db_items[6], 15.0),   # M4A4 | Neo-Noir
        (db_items[9], 10.0),   # AWP | Asiimov
        (db_items[16], 10.0),  # Glock-18 | Fade
    ]

    # Elite Case (1000€) - Legendary and Mythic items
    elite_case_items = [
        (db_items[2], 15.0),   # AK-47 | Fire Serpent
        (db_items[8], 12.0),   # AWP | Dragon Lore
        (db_items[11], 10.0),  # Desert Eagle | Blaze
        (db_items[18], 8.0),   # Karambit | Fade
        (db_items[19], 5.0),   # M9 Bayonet | Crimson Web
    ]

    # AK Specialist Case (750€) - Focus on AK skins
    ak_specialist_items = [
        (db_items[0], 30.0),   # AK-47 | Redline
        (db_items[1], 25.0),   # AK-47 | Vulcan
        (db_items[2], 20.0),   # AK-47 | Fire Serpent
        (db_items[3], 15.0),   # AK-47 | Neon Rider
        (db_items[4], 10.0),   # AK-47 | Jaguar
    ]

    # AWP Specialist Case (800€) - Focus on AWP skins
    awp_specialist_items = [
        (db_items[8], 35.0),   # AWP | Dragon Lore
        (db_items[9], 25.0),   # AWP | Asiimov
        (db_items[10], 20.0),  # AWP | Medusa
        (db_items[11], 15.0),  # AWP | Lightning Strike
        (db_items[12], 5.0),   # AWP | Redline (hypothetical)
    ]

    # Add all case-item relationships
    case_item_relations = [
        (db_cases[0], beginner_case_items),    # Beginner Case
        (db_cases[1], advanced_case_items),    # Advanced Case
        (db_cases[2], elite_case_items),       # Elite Case
        (db_cases[3], ak_specialist_items),    # AK Specialist Case
        (db_cases[4], awp_specialist_items),   # AWP Specialist Case
    ]

    for case_obj, items_list in case_item_relations:
        for item_obj, probability in items_list:
            db_case_item = case_item.CaseItem(
                case_id=case_obj.id,
                item_id=item_obj.id,
                probability=probability
            )
            db.add(db_case_item)

    db.commit()
    db.close()

    print("New database initialized successfully!")

if __name__ == "__main__":
    init_db()