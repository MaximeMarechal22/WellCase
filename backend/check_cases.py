from app.db.session import SessionLocal
from app.models import case, case_item
from sqlalchemy import func

db=SessionLocal()
try:
 rows=db.query(case.Case).filter(case.Case.is_active.is_(True)).order_by(case.Case.id).all()
 print("Active cases:",len(rows))
 for r in rows:
  c=db.query(func.count(case_item.CaseItem.id)).filter(case_item.CaseItem.case_id==r.id).scalar()
  print(f"{r.id}: {r.name} | {r.price:.0f}€ | drops={c}")
finally: db.close()
