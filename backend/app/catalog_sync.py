from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from .models import case, case_item, item
from .db.session import engine


BASE_ITEMS = [
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

BASE_CASES = [
    ("Beginner Case", "Une caisse accessible pour démarrer, avec des drops classiques.", 100.0, "/images/cases/beginner.png", "#3498db"),
    ("Advanced Case", "Un palier supérieur avec des skins plus rares.", 500.0, "/images/cases/advanced.png", "#9b59b6"),
    ("Elite Case", "La caisse haut de gamme pour les gros drops.", 1000.0, "/images/cases/elite.png", "#e74c3c"),
    ("AK Specialist Case", "Dédiée aux amateurs d'AK-47.", 750.0, "/images/cases/ak_specialist.png", "#e67e22"),
    ("AWP Specialist Case", "Dédiée aux amateurs d'AWP.", 800.0, "/images/cases/awp_specialist.png", "#f39c12"),
]

BASE_CASE_REWARDS = {
    "Beginner Case": [("AK-47 | Jaguar",42), ("M4A1-S | Guardian",34), ("Desert Eagle | Crimson Web",18), ("USP-S | Kill Confirmed",5), ("AK-47 | Redline",1)],
    "Advanced Case": [("AK-47 | Redline",25), ("AK-47 | Vulcan",20), ("M4A1-S | Hyper Beast",20), ("M4A4 | Neo-Noir",15), ("AWP | Asiimov",10), ("Glock-18 | Fade",10)],
    "Elite Case": [("AK-47 | Fire Serpent",30), ("AWP | Dragon Lore",22), ("Desert Eagle | Blaze",18), ("Karambit | Fade",15), ("M9 Bayonet | Crimson Web",10), ("Butterfly Knife | Doppler",5), ("Sport Gloves | Pandora's Box",3), ("Driver Gloves | Imperial Plaid",3)],
    "AK Specialist Case": [("AK-47 | Redline",30), ("AK-47 | Vulcan",25), ("AK-47 | Fire Serpent",20), ("AK-47 | Neon Rider",15), ("AK-47 | Jaguar",10)],
    "AWP Specialist Case": [("AWP | Dragon Lore",20), ("AWP | Medusa",20), ("AWP | Asiimov",25), ("AWP | Lightning Strike",35)],
}

NEW_ITEMS = [
    ("AK-47 | Head Shot", "AK", "Covert", 1600.0, "/images/items/ak_head_shot.png", 0.08, "#ef4444"),
    ("M4A1-S | Printstream", "M4", "Covert", 2800.0, "/images/items/m4_printstream.png", 0.07, "#a855f7"),
    ("AWP | Gungnir", "AWP", "Contraband", 7500.0, "/images/items/awp_gungnir.png", 0.04, "#f59e0b"),
    ("Desert Eagle | Printstream", "Desert Eagle", "Covert", 2200.0, "/images/items/deagle_printstream.png", 0.09, "#ef4444"),
    ("Glock-18 | Gamma Doppler", "Glock", "Covert", 2600.0, "/images/items/glock_gamma.png", 0.03, "#22d3ee"),
    ("Karambit | Gamma Doppler", "knife", "Covert", 6000.0, "/images/items/karambit_gamma.png", 0.02, "#34d399"),
    ("M9 Bayonet | Doppler", "knife", "Covert", 5200.0, "/images/items/m9_doppler.png", 0.03, "#60a5fa"),
    ("Sport Gloves | Vice", "gloves", "Extraordinary", 4500.0, "/images/items/sport_vice.png", 0.05, "#ec4899"),
]
NEW_CASES = [
    ("Neon Case", "Des skins modernes avec un jackpot rare, sans rendre le bankroll infini.", 1250.0, "/images/cases/neon.png", "#22d3ee", [("AK-47 | Neon Rider",42),("M4A1-S | Hyper Beast",28),("AK-47 | Head Shot",15),("Desert Eagle | Printstream",8),("M4A1-S | Printstream",5),("Glock-18 | Gamma Doppler",2)]),
    ("Knife Case", "Couteaux rares, avec les très gros drops volontairement exceptionnels.", 1500.0, "/images/cases/knife.png", "#a855f7", [("M9 Bayonet | Crimson Web",60),("Butterfly Knife | Doppler",25),("Karambit | Fade",10),("M9 Bayonet | Doppler",4),("Karambit | Gamma Doppler",1)]),
    ("Covert Case", "Une caisse agressive : beaucoup de pertes, quelques gros coups.", 2000.0, "/images/cases/covert.png", "#ef4444", [("AWP | Asiimov",32),("AK-47 | Fire Serpent",27),("M4A4 | Howl",22),("Desert Eagle | Printstream",10),("AWP | Gungnir",4),("Karambit | Gamma Doppler",3),("AWP | Dragon Lore",2)]),
    ("Supreme Case", "Le haut de gamme WellCase : jackpot très rare et pool premium.", 5000.0, "/images/cases/supreme.png", "#f59e0b", [("M4A4 | Howl",30),("AWP | Dragon Lore",24),("Sport Gloves | Vice",20),("M9 Bayonet | Doppler",13),("Karambit | Gamma Doppler",8),("AWP | Gungnir",4),("M4A1-S | Printstream",1)]),
]

def migrate_compatibility():
    inspector=inspect(engine); tables=inspector.get_table_names()
    if 'users' not in tables:return
    cols={c['name'] for c in inspector.get_columns('users')}
    additions={'avatar_url':'TEXT','xp':'INTEGER DEFAULT 0','open3_tokens':'INTEGER DEFAULT 0','open5_tokens':'INTEGER DEFAULT 0','lifetime_xp':'INTEGER DEFAULT 0','prestige_level':'INTEGER DEFAULT 0',"name_color":"TEXT DEFAULT 'white'","cosmetic_badge":"TEXT","cosmetic_theme":"TEXT DEFAULT 'default'"}
    with engine.begin() as conn:
        for name,ddl in additions.items():
            if name not in cols: conn.execute(text(f'ALTER TABLE users ADD COLUMN {name} {ddl}'))
    if 'inventory' in tables:
        inventory_cols={c['name'] for c in inspector.get_columns('inventory')}
        with engine.begin() as conn:
            if 'upgrade_level' not in inventory_cols:
                conn.execute(text('ALTER TABLE inventory ADD COLUMN upgrade_level INTEGER DEFAULT 0 NOT NULL'))
            if 'condition' not in inventory_cols:
                conn.execute(text("ALTER TABLE inventory ADD COLUMN condition TEXT DEFAULT 'État moyen' NOT NULL"))
    if 'market_listings' in tables:
        market_cols={c['name'] for c in inspector.get_columns('market_listings')}
        with engine.begin() as conn:
            if 'condition' not in market_cols:
                conn.execute(text("ALTER TABLE market_listings ADD COLUMN condition TEXT DEFAULT 'État moyen' NOT NULL"))
def _sync_case_relations(db, row, items_by_name, rewards):
    relations=db.query(case_item.CaseItem).filter(case_item.CaseItem.case_id==row.id).all()
    by_item_id={r.item_id:r for r in relations}
    total=sum(float(p) for _,p in rewards) or 1.0
    desired=set()
    for item_name, prob in rewards:
        obj=items_by_name.get(item_name)
        if not obj:
            continue
        desired.add(obj.id)
        normalized=float(prob)/total*100.0
        rel=by_item_id.get(obj.id)
        if rel is None:
            db.add(case_item.CaseItem(case_id=row.id,item_id=obj.id,probability=normalized))
        elif abs(float(rel.probability or 0)-normalized)>.0001:
            rel.probability=normalized
    for rel in relations:
        if rel.item_id not in desired:
            db.delete(rel)

def _deactivate_retired_cases(db: Session):
    """Hide retired case families from the catalogue.

    Arsenal cases are intentionally retired and must never be recreated by the
    catalogue synchronizer, even when they already exist in a persistent DB.
    Legacy knife cases remain hidden as before.
    """
    rows = db.query(case.Case).filter(case.Case.is_active.is_(True)).all()
    changed = False
    for row in rows:
        name = str(row.name or '').strip().lower()
        if 'arsenal' in name or name in {'knife case', 'solid knife case', 'gloves case'}:
            row.is_active = False
            changed = True
    return changed

def sync_catalog(db:Session):
    changed=False; items_by_name={x.name:x for x in db.query(item.Item).all()}
    if _deactivate_retired_cases(db): changed=True
    # Repair/seed the original catalogue too. This is important on a brand-new
    # Render/Postgres database where the old init script was never run.
    for name,category,rarity,value,image,flt,color in BASE_ITEMS:
        obj=items_by_name.get(name)
        if obj is None:
            obj=item.Item(name=name,category=category,weapon_class=_weapon_class_for(type('X', (), {'category':category,'name':name})()),rarity=rarity,virtual_value=value,image_url=image,float_value=flt,color=color,is_active=True); db.add(obj); db.flush(); items_by_name[name]=obj; changed=True
        else:
            updates={'category':category,'weapon_class':_weapon_class_for(type('X', (), {'category':category,'name':name})()),'rarity':rarity,'virtual_value':value,'image_url':image,'float_value':flt,'color':color,'is_active':True}
            for key,val in updates.items():
                if getattr(obj,key)!=val:
                    setattr(obj,key,val); changed=True
    for name,desc,price,image,color in BASE_CASES:
        row=db.query(case.Case).filter(case.Case.name==name).first()
        if row is None:
            row=case.Case(name=name,description=desc,price=price,image_url=image,color=color,is_active=True); db.add(row); db.flush(); changed=True
        else:
            for key,val in {'description':desc,'price':price,'image_url':image,'color':color,'is_active':True}.items():
                if getattr(row,key)!=val:
                    setattr(row,key,val); changed=True
        before=len(db.query(case_item.CaseItem).filter(case_item.CaseItem.case_id==row.id).all())
        _sync_case_relations(db,row,items_by_name,BASE_CASE_REWARDS[name])
        after=len(db.query(case_item.CaseItem).filter(case_item.CaseItem.case_id==row.id).all())
        if before != after: changed=True

    for name,category,rarity,value,image,flt,color in NEW_ITEMS:
        obj=items_by_name.get(name)
        if obj is None:
            obj=item.Item(name=name,category=category,weapon_class=_weapon_class_for(type('X', (), {'category':category,'name':name})()),rarity=rarity,virtual_value=value,image_url=image,float_value=flt,color=color,is_active=True);db.add(obj);db.flush();items_by_name[name]=obj;changed=True
        else:
            for key,val in {'category':category,'weapon_class':_weapon_class_for(type('X', (), {'category':category,'name':name})()),'rarity':rarity,'virtual_value':value,'image_url':image,'float_value':flt,'color':color,'is_active':True}.items():
                if getattr(obj,key)!=val:setattr(obj,key,val);changed=True
    for obj in items_by_name.values():
        desired_class=_weapon_class_for(obj)
        if obj.weapon_class != desired_class:
            obj.weapon_class=desired_class
            changed=True

    existing={x.name:x for x in db.query(case.Case).all()}
    for name,desc,price,image,color,rewards in NEW_CASES:
        row=existing.get(name)
        if row is None:
            row=case.Case(name=name,description=desc,price=price,image_url=image,color=color,is_active=True);db.add(row);db.flush();existing[name]=row;changed=True
        else:
            for key,val in {'description':desc,'price':price,'image_url':image,'color':color,'is_active':True}.items():
                if getattr(row,key)!=val:setattr(row,key,val);changed=True
        relations=db.query(case_item.CaseItem).filter(case_item.CaseItem.case_id==row.id).all();by_item_id={r.item_id:r for r in relations};total=sum(float(p) for _,p in rewards) or 1.0;desired=set()
        for item_name,prob in rewards:
            obj=items_by_name.get(item_name)
            if not obj:continue
            desired.add(obj.id);normalized=float(prob)/total*100;rel=by_item_id.get(obj.id)
            if rel is None:db.add(case_item.CaseItem(case_id=row.id,item_id=obj.id,probability=normalized));changed=True
            elif abs(float(rel.probability or 0)-normalized)>.0001:rel.probability=normalized;changed=True
        for rel in relations:
            if rel.item_id not in desired:db.delete(rel);changed=True
    if changed:db.commit()
def _weapon_class_for(item_obj):
    c = str(item_obj.category or '').lower()
    n = str(item_obj.name or '').lower()
    if c in {'knife', 'knives'} or 'knife' in n or 'bayonet' in n or 'karambit' in n or 'daggers' in n:
        return 'Knives'
    if c in {'gloves', 'glove'} or 'gloves' in n:
        return 'Gloves'
    if c in {'awp', 'sniper', 'snipers'} or n.startswith(('awp ', 'ssg', 'scar-', 'g3sg1', 'scout')):
        return 'Snipers'
    if c in {'ak', 'm4', 'rifle', 'rifles'} or n.startswith(('ak-', 'm4', 'famas', 'galil', 'aug', 'sg 553')):
        return 'Assault Rifles'
    if c in {'desert eagle', 'glock', 'usp', 'pistol', 'pistols'} or n.startswith(('desert eagle', 'glock', 'usp', 'p250', 'tec-9', 'five-seven')):
        return 'Pistols'
    return 'Other'

def migrate_progression_columns():
    migrate_compatibility()
    inspector=inspect(engine)
    tables=inspector.get_table_names()
    with engine.begin() as conn:
        if 'items' in tables:
            cols={c['name'] for c in inspector.get_columns('items')}
            if 'weapon_class' not in cols:
                conn.execute(text("ALTER TABLE items ADD COLUMN weapon_class TEXT"))
        if 'users' in tables:
            conn.execute(text("UPDATE users SET lifetime_xp = COALESCE(lifetime_xp, xp, 0) WHERE lifetime_xp IS NULL OR lifetime_xp = 0"))
    if 'items' in tables:
        from sqlalchemy.orm import Session
        db=Session(bind=engine)
        try:
            for obj in db.query(item.Item).all():
                if not obj.weapon_class:
                    obj.weapon_class=_weapon_class_for(obj)
            db.commit()
        finally:
            db.close()

