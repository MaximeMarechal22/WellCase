PRESTIGE_XP = 5000

def award_xp(db_user, amount: int):
    amount = max(0, int(amount or 0))
    db_user.xp = int(db_user.xp or 0) + amount
    db_user.lifetime_xp = int(getattr(db_user, 'lifetime_xp', 0) or 0) + amount
    return db_user.xp

def prestige_info(db_user):
    prestige = int(getattr(db_user, 'prestige_level', 0) or 0)
    lifetime = int(getattr(db_user, 'lifetime_xp', 0) or 0)
    return {
        'prestige': prestige,
        'lifetime_xp': lifetime,
        'next_prestige_xp': PRESTIGE_XP,
        'season_xp': int(db_user.xp or 0),
        'ready': int(db_user.xp or 0) >= PRESTIGE_XP,
    }

def collection_completion(db, user_id, weapon_class):
    if not weapon_class:
        return False
    from .models import item as item_model, inventory as inventory_model
    total = db.query(item_model.Item).filter(item_model.Item.is_active.is_(True), item_model.Item.weapon_class == weapon_class).count()
    owned = db.query(inventory_model.Inventory).join(item_model.Item, inventory_model.Inventory.item_id == item_model.Item.id).filter(inventory_model.Inventory.user_id == user_id, inventory_model.Inventory.quantity > 0, item_model.Item.is_active.is_(True), item_model.Item.weapon_class == weapon_class).count()
    return total > 0 and owned >= total
