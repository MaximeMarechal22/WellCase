from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.security import get_current_active_user
from ..db.session import SessionLocal
from ..models import user, case_opening, upgrade, daily_reward, daily_quest, battle_pass
from ..progression_service import award_xp, prestige_info, PRESTIGE_XP

router=APIRouter(); SEASON='2026-S1'
QUESTS=[
 ('open_3','Ouvre 3 caisses','Ouvre 3 caisses aujourd’hui.',3,180,'cases'),
 ('upgrade_2','Réussis 2 upgrades','Réussis 2 upgrades aujourd’hui.',2,220,'successful_upgrades'),
 ('open_5','Enchaîne 5 ouvertures','Atteins 5 ouvertures de caisse aujourd’hui.',5,300,'cases'),
 ('daily_reward','Récupère ton bonus quotidien','Réclame ta récompense quotidienne.',1,120,'daily'),
]
PASS_REWARDS=[
 {'level':1,'xp':500,'type':'cash','amount':250,'label':'+250 €'},
 {'level':2,'xp':1000,'type':'open3','amount':1,'label':'1 ouverture ×3'},
 {'level':3,'xp':1500,'type':'cash','amount':500,'label':'+500 €'},
 {'level':4,'xp':2000,'type':'cosmetic','amount':0,'label':'Nom violet + badge RARE'},
 {'level':5,'xp':2500,'type':'cash','amount':750,'label':'+750 €'},
 {'level':6,'xp':3000,'type':'open3','amount':1,'label':'1 ouverture ×3'},
 {'level':7,'xp':3500,'type':'cosmetic','amount':0,'label':'Thème NEON + badge'},
 {'level':8,'xp':4000,'type':'open5','amount':1,'label':'1 ouverture ×5'},
 {'level':9,'xp':4500,'type':'cash','amount':1500,'label':'+1 500 €'},
 {'level':10,'xp':5000,'type':'cosmetic','amount':0,'label':'Nom OR + badge ELITE'},
]
def get_db():
 db=SessionLocal()
 try: yield db
 finally: db.close()
def day_bounds():
 today=datetime.utcnow().date(); start=datetime.combine(today,datetime.min.time()); return today.isoformat(),start,start+timedelta(days=1)
def progress_for(db,u,metric,start,end):
 if metric=='cases': return db.query(case_opening.CaseOpening).filter(case_opening.CaseOpening.user_id==u.id,case_opening.CaseOpening.opened_at>=start,case_opening.CaseOpening.opened_at<end).count()
 if metric=='successful_upgrades': return db.query(upgrade.Upgrade).filter(upgrade.Upgrade.user_id==u.id,upgrade.Upgrade.upgraded_at>=start,upgrade.Upgrade.upgraded_at<end,upgrade.Upgrade.was_successful.is_(True)).count()
 if metric=='daily': return db.query(daily_reward.DailyReward).filter(daily_reward.DailyReward.user_id==u.id,daily_reward.DailyReward.claimed_at>=start,daily_reward.DailyReward.claimed_at<end).count()
 return 0
def level_from_xp(xp): return min(50,max(1,int(xp//500)+1))
def apply_cosmetics(db_user,xp):
 if db_user.cosmetic_theme=='prestige': return False
 changed=False
 if xp>=2000 and db_user.name_color!='purple': db_user.name_color='purple'; db_user.cosmetic_badge='RARE PASS'; changed=True
 if xp>=3500 and db_user.cosmetic_theme!='neon': db_user.cosmetic_theme='neon'; db_user.cosmetic_badge='NEON'; changed=True
 if xp>=5000 and db_user.name_color!='gold': db_user.name_color='gold'; db_user.cosmetic_badge='BATTLE PASS ELITE'; db_user.cosmetic_theme='gold'; changed=True
 return changed
@router.get('/overview')
def overview(current_user:user.User=Depends(get_current_active_user),db:Session=Depends(get_db)):
 u=db.query(user.User).filter(user.User.id==current_user.id).first(); date_key,start,end=day_bounds(); quests=[]
 for key,title,desc,goal,reward,metric in QUESTS:
  progress=min(goal,progress_for(db,u,metric,start,end)); claimed=db.query(daily_quest.DailyQuestClaim).filter_by(user_id=u.id,quest_key=key,date_key=date_key).first() is not None
  quests.append({'key':key,'title':title,'description':desc,'goal':goal,'progress':progress,'xp_reward':reward,'completed':progress>=goal,'claimed':claimed})
 xp=int(u.xp or 0); apply_cosmetics(u,xp); db.commit()
 claims={r.level for r in db.query(battle_pass.BattlePassClaim).filter_by(user_id=u.id,season=SEASON).all()}
 rewards=[dict(r,unlocked=xp>=r['xp'],claimed=r['level'] in claims) for r in PASS_REWARDS]
 return {'xp':xp,'level':level_from_xp(xp),'next_level_xp':level_from_xp(xp)*500,'season':SEASON,'quests':quests,'battle_pass':rewards,'open3_tokens':u.open3_tokens or 0,'open5_tokens':u.open5_tokens or 0,'cosmetics':{'name_color':u.name_color,'badge':u.cosmetic_badge,'theme':u.cosmetic_theme,'pass_complete':xp>=5000},'prestige':prestige_info(u)}
@router.post('/quests/{quest_key}/claim')
def claim_quest(quest_key:str,current_user:user.User=Depends(get_current_active_user),db:Session=Depends(get_db)):
 d=next((q for q in QUESTS if q[0]==quest_key),None)
 if not d: raise HTTPException(404,'Quête inconnue.')
 key,_,_,goal,reward,metric=d; date_key,start,end=day_bounds()
 if db.query(daily_quest.DailyQuestClaim).filter_by(user_id=current_user.id,quest_key=key,date_key=date_key).first(): raise HTTPException(400,'Quête déjà récupérée aujourd’hui.')
 u=db.query(user.User).filter(user.User.id==current_user.id).first(); progress=progress_for(db,u,metric,start,end)
 if progress<goal: raise HTTPException(400,f'Progression insuffisante : {min(progress,goal)}/{goal}.')
 final=award_xp(u,reward); db.add(daily_quest.DailyQuestClaim(user_id=u.id,quest_key=key,date_key=date_key,xp_reward=reward)); apply_cosmetics(u,final); db.commit(); return {'xp_awarded':reward,'xp':final,'name_color':u.name_color}
@router.post('/battle-pass/{level}/claim')
def claim_pass(level:int,current_user:user.User=Depends(get_current_active_user),db:Session=Depends(get_db)):
 reward=next((r for r in PASS_REWARDS if r['level']==level),None)
 if not reward: raise HTTPException(404,'Niveau de passe introuvable.')
 u=db.query(user.User).filter(user.User.id==current_user.id).first();
 if int(u.xp or 0)<reward['xp']: raise HTTPException(400,'Ce niveau n’est pas encore débloqué.')
 if db.query(battle_pass.BattlePassClaim).filter_by(user_id=u.id,season=SEASON,level=level).first(): raise HTTPException(400,'Récompense déjà récupérée.')
 if reward['type']=='cash': u.virtual_balance=float(u.virtual_balance or 0)+reward['amount']
 elif reward['type']=='open3': u.open3_tokens=int(u.open3_tokens or 0)+1
 elif reward['type']=='open5': u.open5_tokens=int(u.open5_tokens or 0)+1
 elif reward['type']=='cosmetic':
  if level==4: u.name_color='purple'; u.cosmetic_badge='RARE PASS'
  elif level==7: u.cosmetic_theme='neon'; u.cosmetic_badge='NEON'
  elif level==10: u.name_color='gold'; u.cosmetic_badge='BATTLE PASS ELITE'; u.cosmetic_theme='gold'
 db.add(battle_pass.BattlePassClaim(user_id=u.id,season=SEASON,level=level)); db.commit(); return {'reward':reward,'xp':u.xp,'balance':u.virtual_balance,'open3_tokens':u.open3_tokens,'open5_tokens':u.open5_tokens,'name_color':u.name_color,'cosmetic_badge':u.cosmetic_badge,'cosmetic_theme':u.cosmetic_theme}
@router.post('/prestige')
def prestige(current_user:user.User=Depends(get_current_active_user),db:Session=Depends(get_db)):
 u=db.query(user.User).filter(user.User.id==current_user.id).first(); xp=int(u.xp or 0)
 if xp<PRESTIGE_XP: raise HTTPException(400,f'Il faut {PRESTIGE_XP} XP pour passer Prestige.')
 u.prestige_level=int(u.prestige_level or 0)+1; u.xp=0; u.name_color=['#60a5fa','#a78bfa','#f472b6','#f59e0b','#22d3ee'][min(u.prestige_level-1,4)]; u.cosmetic_badge=f'PRESTIGE {u.prestige_level}'; u.cosmetic_theme='prestige'; db.commit(); return {'prestige':u.prestige_level,'xp':0,'lifetime_xp':u.lifetime_xp,'name_color':u.name_color,'badge':u.cosmetic_badge}
