from application import db
from application.models import GameSeries

db.drop_all()
db.create_all()
a = GameSeries(series_name="n/a")
db.session.add(a)
db.session.commit()