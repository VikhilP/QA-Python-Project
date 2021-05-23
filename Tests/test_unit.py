from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
import pytest
import sqlalchemy

#from application import routes
from application import app,db
from application.models import Game, GameSeries,GameForm, SeriesForm
from application.routes import *
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

        db.drop_all()
        db.create_all()
        
        # Create test series
        sampleseries = GameSeries(series_name = "Yakuza")
        sampleseries1 = GameSeries(series_name = "n/a")

        # save game series to database
        
        db.session.add(sampleseries1)
        db.session.add(sampleseries)
        db.session.commit()

        #adding sample games aswell to database
        a = GameSeries.query.filter_by(series_name="Yakuza").first()

        samplegame1 = Game(name="Yakuza 0", series=a.series_name, 
            developer="RGG", game_review=10, release_dateuk = 2015)
        samplegame2 = Game(name="Yakuza Kiwami", series=a.series_name, 
            developer="RGG", game_review=9, release_dateuk = 2016)
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

    # Write a test class for testing that the home page 
    # loads but we are not able to run a get request for 
    # delete and update routes.
class TestViews(TestBase):

    def test_index_get(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 200)

    def test_readgame_get(self):
        response = self.client.get(url_for('readgame'))
        self.assertEqual(response.status_code, 200)
    
    def test_addseries_get(self):
        response = self.client.get(url_for('addseries'))
        self.assertEqual(response.status_code, 200)

    def test_addgame_get(self):
        response = self.client.get(url_for('addgame'))
        self.assertEqual(response.status_code, 200)
    

    

#Test adding 
class TestAdd(TestBase):
    def test_read_game(self):
        response = self.client.post(
            url_for('readgame'),
            data = dict(name="Yakuza 0"),
            follow_redirects=True, 
        )
        self.assertIn(b'Yakuza 0',response.data)

    def test_read_series(self):
        response = self.client.get(
            url_for('index'),
            data = dict(series_name="Yakuza"),
            follow_redirects=True
        )
        self.assertIn(b'Yakuza',response.data)
    
    def test_add_series(self):
        response = self.client.post(
            url_for('addseries'),
            data = dict(series_name = "Fifa"),
            follow_redirects = True
        )
        self.assertIn(b'Fifa', response.data)
        
    def test_add_series_fail(self):
        response = self.client.post(
            url_for('addseries'),
            data = dict(series_name = ""),
            follow_redirects = True
        )
        a = GameSeries.query.all()
        self.assertEqual(len(a), 2)
    
    def test_addgame_with_series(self):
        response = self.client.post(
            url_for('addgame'),
            data = dict(name = "Yakuza 5", series = "Yakuza", developer="RGG", review=8, releasedate = 2012),
            follow_redirects = True
            
        )

        self.assertIn(b"Yakuza 5", response.data)
  
    
    
    def test_add_game_fail(self):
        response = self.client.post(
            url_for('addgame'),
            data = dict(series = "Yakuza", developer="RGG", review=8 , releasedate = 2015 ),
            follow_redirects = True
        )
        a = Game.query.all()

        self.assertEqual(len(a), 2)
    
    def test_update_game(self):
        response = self.client.post(
            url_for('updategame', id=1),
            data = dict(name = "Yakuza 5", series = "Yakuza", developer="RGG", review=8 ,releasedate = 2015 ),
            follow_redirects = True
        )
        self.assertEqual("Yakuza 5", Game.query.get(1).name)

    def test_update_series(self):
        response = self.client.post(
            url_for('updateseries', id=2),
            data = dict(series_name = "Fifa"),
            follow_redirects = True
        )
        self.assertIn(b"Fifa", response.data)

    def test_update_series_readgame(self):
        self.client.post(
            url_for('updateseries', id=2),
            data = dict(series_name = "Fifa"),
            follow_redirects = True
        )
        response = self.client.get(
            url_for('readgame'),
            data = dict(series= "Fifa"),
            follow_redirects=True, 
        )
        self.assertEqual( "Fifa",Game.query.get(1).series)
    
    def test_update_review(self):
        self.client.post(
            url_for('updategame', id=1),
            data = dict(name = "Yakuza 0", series = "Yakuza", developer = "RGG", review=9, releasedate = 2015),
            follow_redirects = True
        )
        self.assertEqual(9.0,GameSeries.query.get(2).series_review)
    
    def test_delete_game(self):
        self.client.post(
            url_for("deleteGame"),
            data = dict(game_id=1),
            follow_redirects = True
        )
        f = len(Game.query.all())
        self.assertEqual(1, f)
        
        self.client.post(
            url_for("deleteGame"),
            data = dict(game_id=2),
            follow_redirects = True
        )
        a = GameSeries.query.filter_by(series_name = "Yakuza").first()
        self.assertEqual(a.first_release, 0)
    
    def test_delete_series(self):
        self.client.post(
            url_for("deleteSeries"),
            data = dict(id=2),
            follow_redirects = True
        )
        f = len(GameSeries.query.all())
        print(f)
        self.assertIs(f, 1)

    
