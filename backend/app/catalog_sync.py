from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from .models import case, case_item, item
from .db.session import engine

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

WEAPON_TYPE_CASES = [
    ('Pistol Arsenal Case', 'Une caisse dédiée aux pistolets, des drops abordables aux pièces les plus rares.', 320.0, '/images/cases/type_pistols.png', '#f59e0b', 'Pistols'),
    ('Rifle Arsenal Case', 'Une caisse dédiée aux fusils d’assaut avec un pool compétitif.', 900.0, '/images/cases/type_rifles.png', '#22d3ee', 'Assault Rifles'),
    ('Sniper Arsenal Case', 'Une caisse de snipers où les gros AWP restent exceptionnels.', 1100.0, '/images/cases/type_snipers.png', '#60a5fa', 'Snipers'),
    ('Knife Arsenal Case', 'Réservée aux couteaux, avec les modèles les plus rares en jackpot.', 2400.0, '/images/cases/type_knives.png', '#a855f7', 'Knives'),
    ('Gloves Arsenal Case', 'Réservée aux gants et à leurs finitions premium.', 1600.0, '/images/cases/type_gloves.png', '#ec4899', 'Gloves'),
]
RARITY_WEIGHTS = {
    'Mil-Spec': 58.0,
    'Restricted': 28.0,
    'Classified': 10.0,
    'Covert': 3.2,
    'Contraband': 0.7,
    'Extraordinary': 0.1,
    'Legendary': 0.3,
    'Mythic': 0.1,
}

def _build_type_case_rewards(items, weapon_class):
    pool=[obj for obj in items if obj.is_active and obj.weapon_class==weapon_class]
    if not pool:
        return []
    raw=[]
    for obj in sorted(pool, key=lambda x: (float(x.virtual_value or 0), x.name.lower())):
        rarity_weight=RARITY_WEIGHTS.get(str(obj.rarity), 1.0)
        value=float(obj.virtual_value or 0)
        # Keep cheap items accessible while pushing expensive/legendary drops down.
        value_factor=max(0.35, min(1.0, 250.0/max(value,250.0)))
        raw_weight=rarity_weight*value_factor
        raw.append((obj.name, raw_weight))
    total=sum(w for _,w in raw) or 1.0
    return [(name, weight/total*100.0) for name,weight in raw]

def migrate_compatibility():
    inspector=inspect(engine); tables=inspector.get_table_names()
    if 'users' not in tables:return
    cols={c['name'] for c in inspector.get_columns('users')}
    additions={'avatar_url':'TEXT','xp':'INTEGER DEFAULT 0','open3_tokens':'INTEGER DEFAULT 0','open5_tokens':'INTEGER DEFAULT 0','lifetime_xp':'INTEGER DEFAULT 0','prestige_level':'INTEGER DEFAULT 0',"name_color":"TEXT DEFAULT 'white'","cosmetic_badge":"TEXT","cosmetic_theme":"TEXT DEFAULT 'default'"}
    with engine.begin() as conn:
        for name,ddl in additions.items():
            if name not in cols: conn.execute(text(f'ALTER TABLE users ADD COLUMN {name} {ddl}'))
def sync_catalog(db:Session):
    changed=False; items_by_name={x.name:x for x in db.query(item.Item).all()}
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
    # One focused case per weapon class. The pools are built from the actual live catalog,
    # so the case automatically stays synchronized when new skins are added.
    for name, desc, price, image, color, weapon_class in WEAPON_TYPE_CASES:
        row=existing.get(name)
        if row is None:
            row=case.Case(name=name,description=desc,price=price,image_url=image,color=color,is_active=True)
            db.add(row); db.flush(); existing[name]=row; changed=True
        else:
            for key,val in {'description':desc,'price':price,'image_url':image,'color':color,'is_active':True}.items():
                if getattr(row,key)!=val:
                    setattr(row,key,val); changed=True
        rewards=_build_type_case_rewards(list(items_by_name.values()), weapon_class)
        relations=db.query(case_item.CaseItem).filter(case_item.CaseItem.case_id==row.id).all()
        by_item_id={r.item_id:r for r in relations}
        desired=set()
        for item_name, prob in rewards:
            obj=items_by_name.get(item_name)
            if not obj: continue
            desired.add(obj.id)
            rel=by_item_id.get(obj.id)
            if rel is None:
                db.add(case_item.CaseItem(case_id=row.id,item_id=obj.id,probability=float(prob))); changed=True
            elif abs(float(rel.probability or 0)-float(prob))>.0001:
                rel.probability=float(prob); changed=True
        for rel in relations:
            if rel.item_id not in desired:
                db.delete(rel); changed=True
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

