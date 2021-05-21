from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
import pytest
import sqlalchemy

#from application import routes
from application import app,db
from application.models import Game, GameSeries,GameForm, SeriesForm
from application.routes import *
from flask import url_for
from flask_testing import LiveServerTestCase

class TestBase(LiveServerTestCase):
    def create_app(self):

        # Pass in testing configurations for the app. Here we use sqlite without a persistent database for our tests.
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
        app.config['SECRET_KEY'] = 'bdfhjs'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = True

        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # Create table

        db.drop_all()
        db.create_all()
        
        # Create test series
        sampleseries = GameSeries(series_name = "Yakuza")

        # save game series to database
        db.session.add(sampleseries)
        db.session.commit()

        #adding sample games aswell to database
        a = GameSeries.query.filter_by(series_name="Yakuza").first()

        samplegame1 = Game(name="Yakuza 0", series=a.series_name, 
            developer="RGG", game_review=10)
        samplegame2 = Game(name="Yakuza Kiwami", series=a.series_name, 
            developer="RGG", game_review=9)
        db.session.add(samplegame1)
        db.session.add(samplegame2)
        db.session.commit()


    def tearDown(self):
        """
        Will be called after every test
        """
        # db.session.delete(GameSeries.query.first())
        # db.session.commit()
        db.session.remove()
        db.drop_all()

class TestExample(TestBase):
    def add_new_game(self):
        self.driver.find_element_by_xpath('/html/body/div[1]/a[3]').click()
        self.assertEqual(url_for('addgame'),self.driver.current_url)
        
