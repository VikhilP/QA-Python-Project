from wtforms.fields.core import IntegerField
from application import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField, DateField

class GameSeries(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    series_name = db.Column(db.String(50), unique = True)
    series_count = db.Column(db.Integer, nullable=False, default = 0)
    # first_release = db.Column(db.Date)
    # latest_release = db.Column(db.Date)
    # abandoned = db.Column(db.Boolean)
    series_review = db.Column(db.Float(), default=0) 
    games = db.relationship("Game", backref="seriesname")

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    series = db.Column(db.String(50), db.ForeignKey("game_series.series_name"),nullable=True)
    developer = db.Column(db.String(50), nullable=False)
    # release_dateuk = db.Column(db.Date)
    #genre = db.Column(db.String(50))
    #age_rating = db.Column(db.String(50)) might be a select field

    game_review = db.Column(db.Integer, default = 0)


class SeriesForm(FlaskForm):
    series_name = StringField('Series Name')
    submit = SubmitField("Add Series")

class GameForm(FlaskForm):
    # all_gameseries = GameSeries.query.all()
    # gameseries_array = [("n/a", "n/a"),]

    # for series in all_gameseries:
    #     gameseries_array.append(tuple((series.series_name, series.series_name)))

    name = StringField('Game Name')
    series = SelectField('Pick Series (if applicable)', choices = [("n/a","n/a"),])
    developer = StringField("Developer") #can turn into a select field just like game series
    # releasedate = DateField("UK Release Year", format = '%Y')
    review = IntegerField("Rating")
    submit = SubmitField("Add Game")


    



