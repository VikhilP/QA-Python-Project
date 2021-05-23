from application import app, db
from application.models import Game, GameSeries, SeriesForm, GameForm
from flask import render_template, request, redirect, url_for #added this as i know i will need it later

@app.route("/")
def index():
    form = SeriesForm()
    # a = GameSeries.query.filter_by(series_name=_series).first()
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
    print(temp)
    db.session.delete(temptask)
    db.session.commit()
    if temptask.series !="n/a":
        count = Game.query.filter_by(series=temptask.series).count()
        series_to_update = GameSeries.query.filter_by(series_name = temptask.series).first()
        series_to_update.series_count = count
        db.session.commit()
        a = GameSeries.query.all()
        for _series in a:
            sum = 0
            b = Game.query.filter_by(series=_series.series_name)
            for game in b:
                sum = sum + game.game_review
            if b.count()!=0 and sum !=0:
                _series.series_review = sum / (b.count())
            elif b.count()==0:
                    _series.series_review = 0.0
                    _series.latest_release = 0
                    _series.first_release = 0

        db.session.commit()
    return redirect(url_for("readgame"))


@app.route('/addgame', methods = ["GET", "POST"])
def addgame():
    error = ""
    form = GameForm()
    all_gameseries = GameSeries.query.all()
    gameseries_array = []

    for series in all_gameseries:
        gameseries_array.append(tuple((series.series_name, series.series_name)))

    form.series.choices=gameseries_array

    if form.validate_on_submit():
        _name = form.name.data
        _series = form.series.data
        _developer = form.developer.data
        _review = form.review.data
        _release = form.releasedate.data

        
        new_game = Game(name = _name, series = _series, developer = _developer, game_review = _review, release_dateuk = _release)
        db.session.add(new_game)
        db.session.commit()
        if _series!= "n/a":
            game_series_to_update = GameSeries.query.filter_by(series_name=_series).first()
            game_series_to_update.series_count += 1
            db.session.commit()
            a = GameSeries.query.all()
            for _series in a:
                sum = 0
                b = Game.query.filter_by(series=_series.series_name)
                print(_series.first_release)
                firstr = int(_series.first_release or 0)
                lastr = int(_series.latest_release or 0)
                for game in b:
                    sum = sum + game.game_review
                    
                    if game.release_dateuk > lastr:
                        _series.latest_release = game.release_dateuk
                        lastr = game.release_dateuk
                        
                    if game.release_dateuk < firstr or firstr == 0:
                        _series.first_release = game.release_dateuk
                        firstr = game.release_dateuk
                
                if b.count()!=0 and sum !=0:
                    _series.series_review = sum / (b.count())
                elif b.count()==0:
                    _series.series_review = 0.0
                    _series.latest_release = 0
                    _series.first_release = 0
            db.session.commit()

        return redirect(url_for("readgame"))
    
    return render_template('addgame.html', form=form, message=error)


@app.route("/updateseries<int:id>", methods=["GET", "POST"])
def updateseries(id):
    error = ""
    series_to_update = GameSeries.query.filter_by(id=id).first()

    form = SeriesForm()

    if form.validate_on_submit():
        _name = form.series_name.data

        old_name = series_to_update.series_name
        # if len(_name) == 0:
        #     error = "Please fill the required fields"
        # else:
        series_to_update.series_name = _name
        db.session.commit()
        all_games_filter = Game.query.filter_by(series=old_name).all()
        for game in all_games_filter:
            game.series = _name
        db.session.commit()
        return redirect(url_for("index"))
    else:
        form.series_name.data = series_to_update.series_name
    return render_template('updateseries.html', form=form, message=error, series=series_to_update)


@app.route("/updategame<int:id>", methods=["GET", "POST"])
def updategame(id):
    error = ""
    game_to_update = Game.query.filter_by(game_id=id).first()
    
    form = GameForm()
    all_gameseries = GameSeries.query.all()

    gameseries_array = [("n/a", "n/a"),]
    for series in all_gameseries:
        gameseries_array.append(tuple((series.series_name, series.series_name)))

    form.series.choices=gameseries_array
    seriesupdate = game_to_update.series

    if form.validate_on_submit():
        _name = form.name.data
        _series = form.series.data
        _developer = form.developer.data
        _review = form.review.data
        _release = form.releasedate.data

        # if len(_name) == 0 or len(_developer) == 0:
        #     error = "Please fill the required fields"
        
        game_to_update.name = _name
        game_to_update.series = _series
        game_to_update.developer = _developer
        game_to_update.game_review = _review
        game_to_update.release_dateuk = _release
        db.session.commit()
            
            
        if seriesupdate != "n/a":
            count = Game.query.filter_by(series=seriesupdate).count()
            old_series_to_update = GameSeries.query.filter_by(series_name = seriesupdate).first()
            old_series_to_update.series_count = count
            db.session.commit()
        if _series != "n/a":
            count = Game.query.filter_by(series=_series).count()
            new_series_to_update = GameSeries.query.filter_by(series_name=_series).first()
            new_series_to_update.series_count = count
            db.session.commit()
        # a = GameSeries.query.all()
        # for _series in a:
        #     sum = 0
        #     b = Game.query.filter_by(series=_series.series_name)
        #     if b.count()>0:
        #         for game in b:
        #             sum = sum + game.game_review
        a = GameSeries.query.all()
        for _series in a:
            sum = 0
            b = Game.query.filter_by(series=_series.series_name)
            print(_series.first_release)
            firstr = int(_series.first_release or 0)
            lastr = int(_series.latest_release or 0)
            for game in b:
                sum = sum + game.game_review
                
                if game.release_dateuk > lastr:
                    _series.latest_release = game.release_dateuk
                    game.release_dateuk = firstr

                if game.release_dateuk < firstr or firstr == 0:
                    _series.first_release = game.release_dateuk
                    game.release_dateuk = firstr
                if b.count()!=0 and sum !=0:
                    _series.series_review = sum / (b.count())
                elif b.count()==0:
                    _series.series_review = 0.0
                    _series.latest_release = 0
                    _series.first_release = 0
        db.session.commit()
        return redirect(url_for("readgame"))
    else:
        form.name.data = game_to_update.name
        form.series.data = game_to_update.series
        form.developer.data = game_to_update.developer
        form.review.data = game_to_update.game_review
        form.releasedate.data = game_to_update.release_dateuk
    return render_template('updategame.html', form=form, message=error, game=game_to_update)

@app.route("/readgame", methods=["GET", "POST"])
def readgame():
    form = GameForm()
    all_games_sorted = Game.query.order_by(Game.series).order_by(Game.name).all() 

    return render_template("readgame.html", form=form, all_games = all_games_sorted )

@app.route('/addseries', methods = ["GET", "POST"])
def addseries():
    error = ""
    form = SeriesForm()
    if form.validate_on_submit():
        _series = form.series_name.data
        a = GameSeries.query.all()
        b = []
        for series in a:
            b.append(series.series_name)
        if _series in b:
            error = "That series has already been used"
        else:
            new_series = GameSeries(series_name = _series)
            db.session.add(new_series)
            db.session.commit()
            return redirect(url_for("index"))
            
    return render_template('addseries.html', form=form, message=error)



