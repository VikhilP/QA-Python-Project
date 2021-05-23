from wtforms.fields.core import IntegerField
from application import db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField, DateField
from wtforms.validators import *
from application.validators import *


class GameSeries(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    series_name = db.Column(db.String(50), unique = True)
    series_count = db.Column(db.Integer, nullable=False, default = 0)
    first_release = db.Column(db.Integer, default = 0) 
    latest_release = db.Column(db.Integer, default = 0)
    # abandoned = db.Column(db.Boolean)
    series_review = db.Column(db.Float(), default=0) 
    games = db.relationship("Game", backref="seriesname")

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    series = db.Column(db.String(50), db.ForeignKey("game_series.series_name"),nullable=True)
    developer = db.Column(db.String(50), nullable=False)
    release_dateuk = db.Column(db.Integer, nullable = False)
    # genre = db.Column(db.String(50))
    # age_rating = db.Column(db.String(50)) might be a select field

    game_review = db.Column(db.Integer, default = 0)


class SeriesForm(FlaskForm):
    
    series_name = StringField('Series Name', validators=[DataRequired()])
    submit = SubmitField("Add Series")



class GameForm(FlaskForm):
    name = StringField('Game Name', validators=[DataRequired()])
    series = SelectField('Pick Series (if applicable)', choices = [("n/a","n/a"),])
    developer = StringField("Developer", validators=[DataRequired()]) #can turn into a select field just like game series
    releasedate = StringField("UK Release Year", validators=[DataRequired(), Length(min= 4, max= 4, message="Release date must be in YYYY format")])
    review = IntegerField("Rating", [NumberRange(min=0 ,max=10, message="Rating must be between 0 and 10")])
    submit = SubmitField("Add Game")


    



