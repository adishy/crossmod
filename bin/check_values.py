from crossmod.ml.classifiers import CrossmodClassifiers
from crossmod.db.interface import CrossmodDB
from crossmod.db.tables import DataTable
from crossmod.helpers.consts import CrossmodConsts
from datetime import datetime, timedelta 

db = CrossmodDB()
#classifiers = CrossmodClassifiers()
last_week = datetime.now() - timedelta(weeks = 1)
count = 0
for row in db.database_session.query(DataTable).filter(DataTable.ingested_utc >= last_week).all():
  if row.crossmod_action == "filtered":
    print("Skipping")
    continue

  print(f"Modifying row: {count}, comment id: {row.id}, ingested_utc: {row.ingested_utc}")

  #result = classifiers.get_result(row.body)
  #row.agreement_score = result['agreement_score']
  #row.norm_violation_score = result['norm_violation_score']
  
  if row.agreement_score >= 0.85:
    row.crossmod_action = "report"

  count += 1

db.database_session.commit()
db.database_session.exit()
