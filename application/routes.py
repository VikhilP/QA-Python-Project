from application import app, db
from application.models import Game, GameSeries, SeriesForm

from flask import render_template, request, redirect, url_for #added this as i know i will need it later

# @app.route("/")
# def readseries():
#     return "Testing 1 2 3"
@app.route('/addseries')
def addseries():
    error = ""
    form = SeriesForm()

    if request.method == "POST":
        series_name = form.series_name.data
        

        if len(series_name) == 0:
            error = "Please enter the series name"
        else:
            new_series = GameSeries(series_name = form.series_name.data, review = form.review.data)
            db.session.add(new_series)
            db.session.commit()
            return redirect(url_for("/"))
    
    return render_template('addseries.html', form=form, message=error)



