from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField,SelectField
from wtforms.validators import DataRequired
import requests
from Prediction import prediction


movie_key = "e35b8f1415cec2229f2b61f89ea5db75"

movie_url = "https://api.themoviedb.org/3/search/movie"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap(app)

##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///NEW_MOVIE_1.db'
db = SQLAlchemy()
db.init_app(app)

class MOVIE(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float)
    votes_average = db.Column(db.Float)
    img_url = db.Column(db.String(250), nullable=False)
    actor = db.Column(db.String(250))

class MOVIE_PREDICT1(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique = False)
    movie = db.Column(db.String(250), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    actor = db.Column(db.String(250),unique=False,nullable=False)
    votes = db.Column(db.Integer, nullable=False)
    predict = db.Column(db.Integer, nullable=False)
with app.app_context():
    db.create_all()

class AddMovie(FlaskForm):
    show = StringField("Add Your Show Here!!!")
    submit = SubmitField()


class AddActor(FlaskForm):
    actor = SelectField(u"Enter Your Choice",choices=[('Salman Khan',"SALMAN KHAN"),('Shahruk Khan',"SHAHRUKH KHAN")])
    submit = SubmitField()

class AddData(FlaskForm):
    actor = SelectField(u"Enter Your Choice",choices=[('Salman Khan',"SALMAN KHAN"),('Shah Rukh Khan',"SHAHRUKH KHAN")])
    votes = StringField("Entry No of Votes")
    submit = SubmitField()


@app.route("/")
def home():
    result = db.session.execute(db.select(MOVIE))
    all_shows = result.scalars()
    actor1 = []
    actor2 =[]
    
    for i in all_shows:
        if i.actor == "Salman Khan":
            actor1.append(i)
        elif i.actor == "Shahruk Khan":
            actor2.append(i)    
    return render_template("index.html",actor1 = actor1,actor2 =actor2)

@app.route("/display")
def display_data():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_key_api_url = f"https://api.themoviedb.org/3/movie/{movie_api_id}"
        response = requests.get(movie_key_api_url,params={"api_key":movie_key,"language": "en-US"})
        data = response.json()
        return render_template("list.html",details=data)

@app.route("/search",methods=['GET','POST'])
def search_movie():
    form = AddMovie()
    if form.validate_on_submit():
        movie_name = form.show.data
        response = requests.get(movie_url,params={"api_key":movie_key,"query":movie_name})
        data = response.json()["results"]
        return render_template("add.html",option=data,form=form)
    return render_template("add.html",form=form)


@app.route("/rate")
def rate_movie():
    movie_id = request.args.get("id")
    movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(movie_api_url,params={"api_key":movie_key,"language": "en-US"})
    data = response.json()
    new_movie = MOVIE(
                id = data["id"],
                title = data["title"], 
                year=data["release_date"],
                rating = data["popularity"],
                votes_average = data["vote_average"],
                img_url = data["poster_path"],
                description=data["overview"],
            )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("add_rating",id=new_movie.id))

@app.route("/movie",methods=['GET','POST'])
def add_rating():    
    movie_id = request.args.get("id")
    form = AddActor()
    movie = db.get_or_404(MOVIE, movie_id)
    if form.validate_on_submit():
        movie.actor = form.actor.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("movie.html",form=form)


@app.route("/delete")
def delete_show():
    movie_id = request.args.get("id")
    movie_to_delete = db.get_or_404(MOVIE,movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/search_predict",methods=['GET','POST'])
def search_predict_movie():
    form = AddMovie()
    if form.validate_on_submit():
        movie_name = form.show.data
        response = requests.get(movie_url,params={"api_key":movie_key,"query":movie_name})
        data = response.json()["results"]
        return render_template("add_predict.html",option=data,form=form)
    return render_template("add_predict.html",form=form)

@app.route("/predict_select",methods=['GET','POST'])
def predict_select():
    form = AddData()
    movie_id = request.args.get("id")
    movie_api_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    response = requests.get(movie_api_url,params={"api_key":movie_key,"language": "en-US"})
    data = response.json()
    if form.validate_on_submit():
        year = data["release_date"].split("-")[0]
        votes = form.votes.data
        actor = form.actor.data
        predict = prediction(actor=actor,votes=votes,year=year)
        new_movie_predict = MOVIE_PREDICT1(
                id = data["id"],
                movie = data["title"], 
                year=year,
                actor = actor,
                votes = votes,
                predict = predict
            )
        db.session.add(new_movie_predict)
        db.session.commit()
        return redirect(url_for('predict_movie'))
    return render_template("add_predict.html",form=form)

@app.route("/predict_movie")
def predict_movie():
    result = db.session.execute(db.select(MOVIE_PREDICT1))
    a = result.scalars()
    print(a)
    for i in a:
        predict = i.predict
    return render_template("movie_predict",predict=predict)

if __name__ == '__main__':
    app.run(debug=True)
