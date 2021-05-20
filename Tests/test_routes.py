from flask_sqlalchemy import SQLAlchemy
import pytest
import sqlalchemy

#from application import routes
from application import app,db
from application.models import Game, GameSeries,GameForm, SeriesForm
from flask import url_for
from flask_testing import TestCase


# Create the base class
class TestBase(TestCase):
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
        # if len(GameSeries.query.all())>0:
        #     db.session.delete(GameSeries.query.first())
        #     db.session.commit()
        db.drop_all()
        db.create_all()
        print(GameSeries.query.all())
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
        db.session.delete(GameSeries.query.first())
        db.session.commit()
        db.session.remove()
        db.drop_all()

    # Write a test class for testing that the home page 
    # loads but we are not able to run a get request for 
    # delete and update routes.
class TestViews(TestBase):

    def test_index_get(self):
        response = self.client.get(url_for('index'))
        print(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertEqual(response.status_code, 200)

    def test_readgame_get(self):
        response = self.client.get(url_for('readgame'))
        print(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertEqual(response.status_code, 200)
    
    def test_addseries_get(self):
        response = self.client.get(url_for('addseries'))
        print(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertEqual(response.status_code, 200)

    def test_addgame_get(self):
        response = self.client.get(url_for('addgame'))
        print(app.config["SQLALCHEMY_DATABASE_URI"])
        self.assertEqual(response.status_code, 200)
    

    

#Test adding 
# class TestAdd(TestBase):
#     def test_add_post(self):
#         response = self.client.post(
#             url_for('home'),
#             data = dict(name="MrMan"),
#             follow_redirects=True
#         )
#         self.assertIn(b'MrMan',response.data)