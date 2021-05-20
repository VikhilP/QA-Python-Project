import pytest

#from application import routes
from application import app,db
from application.models import *
from flask import url_for
from flask_testing import TestCase


# Create the base class
class TestBase(TestCase):
    def create_app(self):

        # Pass in testing configurations for the app. Here we use sqlite without a persistent database for our tests.
        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='TEST_SECRET_KEY',
                DEBUG=True,
                WTF_CSRF_ENABLED=False
                )
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # Create table
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

    def test_addgame_get(self):
        response = self.client.get(url_for('addgame'))
        self.assertEqual(response.status_code, 200)

    def test_addseries_get(self):
        response = self.client.get(url_for('addseries'))
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