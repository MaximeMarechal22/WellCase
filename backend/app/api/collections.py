from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from ..db.session import SessionLocal
from ..core.security import get_current_active_user
from ..models import item, inventory, user

router=APIRouter()
CLASSES=[
    ('Assault Rifles','Fusils d’assaut','+25 XP sur chaque ouverture de cette catégorie','RIFLE SPECIALIST'),
    ('Snipers','Snipers','+25 XP sur chaque ouverture de cette catégorie','SNIPER SPECIALIST'),
    ('Pistols','Pistolets','+25 XP sur chaque ouverture de cette catégorie','PISTOL SPECIALIST'),
    ('Knives','Couteaux','Badge exclusif de collection','KNIFE COLLECTOR'),
    ('Gloves','Gants','Badge exclusif de collection','GLOVE COLLECTOR'),
]
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
@router.get('/overview')
def overview(current_user:user.User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    owned={x.item_id for x in db.query(inventory.Inventory).filter(inventory.Inventory.user_id==current_user.id,inventory.Inventory.quantity>0).all()}
    active=db.query(item.Item).filter(item.Item.is_active.is_(True)).all()
    out=[]
    for key,label,bonus,badge in CLASSES:
        pool=sorted([x for x in active if x.weapon_class==key], key=lambda x: (-float(x.virtual_value or 0), x.name.lower()))
        item_rows=[{'id':x.id,'name':x.name,'category':x.category,'weapon_class':x.weapon_class,'rarity':x.rarity,'virtual_value':x.virtual_value,'image_url':x.image_url,'owned':x.id in owned} for x in pool]
        have=sum(1 for x in pool if x.id in owned)
        complete=bool(pool) and have==len(pool)
        out.append({'key':key,'label':label,'owned':have,'total':len(pool),'complete':complete,'bonus':bonus,'badge':badge,'items':item_rows})
    return {'collections':out}
