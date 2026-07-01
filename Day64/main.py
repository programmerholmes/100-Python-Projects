from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from socks import method
from sqlalchemy.util import methods_equivalent
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
import requests
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



TMDB_API_KEY = "YOUR_TMDB_API_KEY"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

# For the second URL for complete description and high quality poster of the movie selected
MOVIE_INFO_URL = "https://api.themoviedb.org/3/movie"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"




app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY_HERE'
Bootstrap(app)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"

db.init_app(app)



class Movies(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(500), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()

    # Updated the url link
    # movie_to_update = db.session.execute(db.select(Movies).where(Movies.title == "Avatar The Way of Water")).scalar()
    # movie_to_update.img_url = "https://media.themoviedb.org/t/p/w600_and_h900_face/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
    # db.session.commit()

    # Just checking
    # new_movie = Movies(
    #     title="Avatar The Way of Water",
    #     year=2022,
    #     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #     rating=7.3,
    #     ranking=10,
    #     review="I liked the water.",
    #     img_url="https://image.tmdb.org/t/p/w500/t6SpguC0B0ubllnu7PShotAnMEw.jpg"
    # )

    # db.session.add(new_movie)
    # db.session.commit()


class UpdateForm(FlaskForm):
    new_rating = StringField("Your Rating out of 10 e.g 7.5", validators=[DataRequired()])
    new_review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")

class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():

    # This was simple
    # results = db.session.execute(db.select(Movies))
    # all_movies = results.scalars().all()

    # Now for the ranking
    all_movies = db.session.execute(db.select(Movies).order_by(Movies.rating)).scalars().all()
    for i in range(len(all_movies)):
        # If we have 10 movies, the first one gets rank 10, the last one gets rank 1
        all_movies[i].ranking = len(all_movies) - i

    db.session.commit()

    ordered_movies = db.session.execute(db.select(Movies).order_by(Movies.ranking)).scalars().all()
    return render_template("index.html", movies=ordered_movies)


@app.route("/add", methods= ["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        print(f"Searching for: {movie_title}")

        response = requests.get(url=TMDB_SEARCH_URL, params={ "api_key": TMDB_API_KEY,
                                                              "query": movie_title
                                                                })

        data = response.json()["results"]
        print(data)

        return render_template("select.html", options=data)

    return render_template("add.html", form = form )


@app.route("/find")
def find_movie():
    tmdb_id = request.args.get('id')

    if tmdb_id:
        response = requests.get(f"{MOVIE_INFO_URL}/{tmdb_id}", params={"api_key": TMDB_API_KEY})
        data = response.json()

        new_movie = Movies(
            title = data["title"],
            year = data["release_date"].split("-")[0],
            img_url = f"{IMAGE_URL}{data['poster_path']}",
            description = data["overview"],
            rating = 0,
            ranking = 0,
            review = "None"
        )
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for("edit", id=new_movie.id))






@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    form = UpdateForm()
    movie_to_update = db.session.get(Movies, id)

    if form.validate_on_submit():
        movie_to_update.rating = float(form.new_rating.data)     # if this was a HTML form , then request.form['name']
        movie_to_update.review = form.new_review.data           # this is how it would have been hehe
        print("Success")

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", movie = movie_to_update, form = form )


@app.route("/delete/<int:id>")              # GET is by default, so it's okay if you don't write it
def delete(id):

    movie_to_delete = db.session.get(Movies, id)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
