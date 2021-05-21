from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
import pytest
import sqlalchemy
from selenium import webdriver
from urllib.request import urlopen

#from application import routes
from application import app,db
from application.models import Game, GameSeries,GameForm, SeriesForm
from application.routes import *
from flask import url_for
from flask_testing import LiveServerTestCase

class TestBase(LiveServerTestCase):
    TEST_PORT = 5050 # test port, doesn't need to be open

    def create_app(self):

        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            LIVESERVER_PORT=self.TEST_PORT,
            
            DEBUG=True,
            TESTING=True
        )

        return app

    def setUp(self):

        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)

        db.create_all() # create schema before we try to get the page
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

        self.driver.get(f'http://localhost:{self.TEST_PORT}')

    def tearDown(self):
        self.driver.quit()

        db.drop_all()

class TestExample(TestBase):
    def test_add_new_game(self):
        self.driver.find_element_by_xpath('/html/body/div[1]/a[3]').click()
        self.assertIn(url_for('addgame'),self.driver.current_url)

        #Game Name
        self.driver.find_element_by_xpath('//*[@id="name"]').send_keys("Rocket League")
        #Developer
        self.driver.find_element_by_xpath('//*[@id="developer"]').send_keys("Psionix")
        #review
        self.driver.find_element_by_xpath('//*[@id="review"]').send_keys(8)
        #Submit
        self.driver.find_element_by_xpath('//*[@id="submit"]').click

        self.assertIn(url_for('readgame'),self.driver.current_url)
        
        self.assertEqual("Rocket League", Game.query.filter_by(game_id=3).name)
        
