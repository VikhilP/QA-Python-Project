from application import app, db
from application.models import Game, GameSeries

from flask import render_template, request, redirect, url_for #added this as i know i will need it later

@app.route("/")
def readseries():
    return "Testing 1 2 3"


