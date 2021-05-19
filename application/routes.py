from application import app, db
from application.models import Game, GameSeries, SeriesForm, GameForm
from flask import render_template, request, redirect, url_for #added this as i know i will need it later

@app.route("/")
def index():
    form = SeriesForm()
    return render_template("index.html", form=form, all_series = GameSeries.query.all() )

@app.route('/deleteseries', methods=["POST"])
def deleteSeries():
    temp = request.form.get("id")
    temptask = GameSeries.query.filter_by(id=temp).first()
    all_games = Game.query.filter_by(series=temptask.series_name).all()
    db.session.delete(temptask)
    db.session.commit()
    print(all_games)
    for game in all_games:
        game.series = "n/a"
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/deletegame', methods=["POST"])
def deleteGame():
    temp = request.form.get("game_id")
    temptask = Game.query.filter_by(game_id=temp).first()
    db.session.delete(temptask)
    
    db.session.commit()
    if temptask.series !="n/a":
        count = Game.query.filter_by(series=temptask.series).count()
        series_to_update = GameSeries.query.filter_by(series_name = temptask.series).first()
        series_to_update.series_count = count
        db.session.commit()
    return redirect(url_for("readgame"))

@app.route('/addgame', methods = ["GET", "POST"])
def addgame():
    error = ""
    form = GameForm()
    all_gameseries = GameSeries.query.all()
    gameseries_array = [("n/a", "n/a"),]

    for series in all_gameseries:
        gameseries_array.append(tuple((series.series_name, series.series_name)))

    form.series.choices=gameseries_array

    if request.method == "POST":
        _name = form.name.data
        _series = form.series.data
        _developer = form.developer.data

        if len(_name) == 0:
            error = "Please enter a game name"
        elif len(_developer) == 0:
            error = "Please enter a developer name"
        else:
            new_game = Game(name = _name, series = _series, developer = _developer)
            db.session.add(new_game)
            db.session.commit()
            if _series!= "n/a":
                game_series_to_update = GameSeries.query.filter_by(series_name=_series).first()
                game_series_to_update.series_count += 1
                db.session.commit()
            return redirect(url_for("readgame"))
    
    return render_template('addgame.html', form=form, message=error)

@app.route("/readgame")
def readgame():
    form = GameForm()
 
    all_games_sorted = Game.query.order_by(Game.series).order_by(Game.name).all() 
    
    return render_template("readgame.html", form=form, all_games = all_games_sorted )




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



