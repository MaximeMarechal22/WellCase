from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from ..db.session import SessionLocal
from ..core.security import get_current_active_user
from ..models import market_listing, inventory, user, item
from ..schemas import market as market_schema
from ..condition_service import effective_value

router = APIRouter()

def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()

def serialize(row, current_id):
    return {
        'id': row.id, 'seller_id': row.seller_id,
        'seller_username': row.seller.username if row.seller else 'Player',
        'item_id': row.item_id, 'price': float(row.price), 'condition': row.condition or 'État moyen', 'effective_value': effective_value(row.item.virtual_value, row.condition), 'created_at': row.created_at,
        'item': row.item, 'is_mine': row.seller_id == current_id,
    }

@router.get('/', response_model=list[market_schema.MarketListing])
def listings(search: str = '', weapon_class: str = '', sort: str = 'newest', limit: int = 100,
             current_user: user.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    q=db.query(market_listing.MarketListing).options(joinedload(market_listing.MarketListing.item), joinedload(market_listing.MarketListing.seller)).filter(market_listing.MarketListing.is_active.is_(True))
    if search.strip():
        term=f"%{search.strip()}%"
        q=q.join(item.Item, market_listing.MarketListing.item).filter(item.Item.name.ilike(term))
    if weapon_class:
        q=q.filter(market_listing.MarketListing.item.has(weapon_class=weapon_class))
    if sort == 'price_asc': q=q.order_by(market_listing.MarketListing.price.asc())
    elif sort == 'price_desc': q=q.order_by(market_listing.MarketListing.price.desc())
    else: q=q.order_by(desc(market_listing.MarketListing.created_at))
    return [serialize(x,current_user.id) for x in q.limit(max(1,min(limit,200))).all()]

@router.post('/', response_model=market_schema.MarketListing)
def create_listing(payload: market_schema.MarketListingCreate, current_user: user.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    inv=db.query(inventory.Inventory).options(joinedload(inventory.Inventory.item)).filter(
        inventory.Inventory.id==payload.inventory_id,
        inventory.Inventory.user_id==current_user.id,
    ).first()
    if not inv or not inv.item:
        raise HTTPException(404,'Skin introuvable dans ton inventaire.')
    if inv.quantity < 1:
        raise HTTPException(400,'Cette skin n’est plus disponible.')
    item_obj = inv.item
    item_id = inv.item_id
    price = round(float(payload.price), 2)
    row = market_listing.MarketListing(
        seller_id=current_user.id,
        item_id=item_id,
        price=price,
        condition=inv.condition or 'État moyen',
        is_active=True,
    )
    inv.quantity -= 1
    if inv.quantity <= 0:
        db.delete(inv)
    db.add(row)
    try:
        db.flush()
        db.refresh(row)
        response = {
            'id': row.id,
            'seller_id': current_user.id,
            'seller_username': current_user.username,
            'item_id': item_id,
            'price': price,
            'created_at': row.created_at,
            'item': item_obj,
            'condition': inv.condition,
            'effective_value': effective_value(item_obj.virtual_value, inv.condition),
            'is_mine': True,
        }
        db.commit()
        return response
    except Exception:
        db.rollback()
        raise HTTPException(500,'Impossible de publier l’annonce.')

@router.post('/{listing_id}/buy')
def buy_listing(listing_id:int,current_user:user.User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    row=db.query(market_listing.MarketListing).options(joinedload(market_listing.MarketListing.item),joinedload(market_listing.MarketListing.seller)).filter(market_listing.MarketListing.id==listing_id,market_listing.MarketListing.is_active.is_(True)).first()
    if not row: raise HTTPException(404,'Annonce introuvable ou déjà vendue.')
    if row.seller_id==current_user.id: raise HTTPException(400,'Tu ne peux pas acheter ta propre annonce.')
    buyer=db.query(user.User).filter(user.User.id==current_user.id).first(); seller=db.query(user.User).filter(user.User.id==row.seller_id).first()
    if not seller: raise HTTPException(404,'Vendeur introuvable.')
    price=float(row.price)
    if float(buyer.virtual_balance or 0)<price: raise HTTPException(400,'Solde insuffisant.')
    try:
        buyer.virtual_balance=float(buyer.virtual_balance or 0)-price
        seller.virtual_balance=float(seller.virtual_balance or 0)+price
        owned=db.query(inventory.Inventory).filter(inventory.Inventory.user_id==buyer.id,inventory.Inventory.item_id==row.item_id,inventory.Inventory.condition==row.condition).first()
        if owned: owned.quantity += 1
        else: db.add(inventory.Inventory(user_id=buyer.id,item_id=row.item_id,quantity=1,condition=row.condition or 'État moyen'))
        row.is_active=False
        db.commit()
    except Exception:
        db.rollback(); raise HTTPException(500,'Achat impossible.')
    return {'success':True,'price':price,'balance_after':float(buyer.virtual_balance),'item':row.item,'seller_username':seller.username}

@router.post('/{listing_id}/cancel')
def cancel_listing(listing_id:int,current_user:user.User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    row=db.query(market_listing.MarketListing).filter(market_listing.MarketListing.id==listing_id,market_listing.MarketListing.seller_id==current_user.id,market_listing.MarketListing.is_active.is_(True)).first()
    if not row: raise HTTPException(404,'Annonce introuvable.')
    owned=db.query(inventory.Inventory).filter(inventory.Inventory.user_id==current_user.id,inventory.Inventory.item_id==row.item_id,inventory.Inventory.condition==row.condition).first()
    if owned: owned.quantity += 1
    else: db.add(inventory.Inventory(user_id=current_user.id,item_id=row.item_id,quantity=1,condition=row.condition or 'État moyen'))
    row.is_active=False; db.commit()
    return {'success':True}
