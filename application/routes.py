from application import app, db
from application.models import Game, GameSeries, SeriesForm

from flask import render_template, request, redirect, url_for #added this as i know i will need it later

@app.route("/")
def index():
    form = SeriesForm()
    return render_template("index.html", form=form, all_series = GameSeries.query.all() )

@app.route('/addseries', methods = ["GET", "POST"])
def addseries():
    error = ""
    form = SeriesForm()

    if request.method == "POST":
        series_name = form.series_name.data
        

        if len(series_name) == 0:
            error = "Please enter the series name"
        else:
            new_series = GameSeries(series_name = form.series_name.data)
            db.session.add(new_series)
            db.session.commit()
            return redirect(url_for("index"))
    
    return render_template('addseries.html', form=form, message=error)



