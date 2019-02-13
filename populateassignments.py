from run import db
from models.network_model import PoolAssignments


i = 1
while i < 229:
  assignment = PoolAssignments.query.get(i)
  assignment.status = 3
  print("Updated assignment number : " + repr(i))
  print(i)
  db.session.commit()
  i += 1
