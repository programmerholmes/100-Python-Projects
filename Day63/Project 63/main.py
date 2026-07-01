from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float



app = Flask(__name__)



class Base(DeclarativeBase):
    pass

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Create a new Table
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    # def __repr__(self):
    #     return f'<Book {self.title}>'

with app.app_context():
    db.create_all()




@app.route('/')
def home():

    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().all()
    return render_template("index.html", all_the_books = all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )                                               # updated from a dict, dict doesn't work here

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    book_to_update = db.session.get(Book, id)

    if request.method == "POST":
        book_to_update.rating = float(request.form["rating"])
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit_rating.html", book = book_to_update)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    book_to_delete = db.session.get(Book, id)
    db.session.delete(book_to_delete)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

