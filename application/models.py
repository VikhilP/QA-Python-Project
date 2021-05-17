from enum import unique
from application import db


class GameSeries(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    series_name = db.Column(db.String(50), unique = True)
    series_count = db.Column(db.Integer, nullable=False)
    first_release = db.Column(db.Date)
    latest_release = db.Column(db.Date)
    series_review = db.Column(db.String(50), default = "0/10")
    games = db.relationship("Game", backref="seriesname")

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    series = db.Column(db.String(50), db.ForeignKey("game_series.series_name"))
    developer = db.Column(db.String(50), nullable=False)
    release_dateuk = db.Column(db.Date)
    game_review = db.Column(db.String(50), default = "0/10")

    



