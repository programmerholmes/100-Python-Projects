# import sqlite3
#
# db = sqlite3.connect("books-collection.db")
#
# cursor = db.cursor()
#
#
# # cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, "
# #                "author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

class Base(DeclarativeBase):
    pass

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"

#Optional: But it will silence the deprecation warning in the console.
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


    # We added the first book manually here, the rest of the books are going to be from the site directly, just for checking
    # new_book = Book(title="Harry Potter", author="J.K. Rowling", rating=9.3)
    #
    # try:
    #     db.session.add(new_book)
    #     db.session.commit()
    #     print("Success!")
    # except IntegrityError:
    #     # This happens if the 'unique' constraint is hit (book already exists)
    #     db.session.rollback()  # This "undoes" the failed add to keep the session clean
    #     print("This book is already in the database!")

    # db.session.execute(db.select(Book)).scalars().all()
    # book = db.session.get(Book, 1)
    # print(book.title)  # This output appears in the PyCharm Console
    # db.session.execute(db.select(Book).where(Book.title == "Harry Potter")).scalar()

    # # 1. Find the book you want to change
    # book_to_update = db.session.get(Book, 1)
    #
    # # 2. Change the value just like a normal Python object
    # book_to_update.rating = 10.0
    #
    # # 3. Commit the change
    # db.session.commit()
    # print("Rating updated!")


    # # 1. Find the book
    # book_to_delete = db.session.get(Book, 1)
    #
    # # 2. Delete it
    # db.session.delete(book_to_delete)
    #
    # # 3. Commit the change
    # db.session.commit()
    # print("Book deleted!")

    # Create
    # db.session.add(object)
    # A new row is born in the.db file.
    #
    # Read
    # db.session.execute(db.select())
    # Python fetches data to show the user.
    #
    # Update
    # book.rating = 10
    # An existing row is modified.
    #
    # Delete
    # db.session.delete(object)
    # A row is permanently removed.

    # while working with Flask, there were 3 ways of creating forms, one was the old html form template,
    # then the other was form.field.label method, and the 3rd was the simplest wtf.quick_form(form).So far am i right?
    # Then i noticed that when you are working with the regular html forms you need that request.form and also you have
    # to have the correct "name", and you also need an if request.method == POST, but when you are working with those
    #     other two, then they have an exact same process, you create a form class and add everything you want
    #     in the main.py, then you can also add the validators to that very class as well, and also you simply
    #     write form.validate_on_submit, no need for those if == "POST" conditions, and yeah you also need those
    #     {{ form.csrf_token }} for the wtf forms, both of them, not both only when you are creating the form manually .
    #   if you do {{ wtf.quick_form(form) }}, then it is automatically done for you. request.form["name"] for html form
    #  data retrieval and form.field.data for wtfroms. data is a label as well.


"""
    The Difference: [] vs .get()
request.form['email']: This is like looking into a standard Python dictionary.

The Risk: If for some reason the HTML form doesn't have a field named "email" 
(maybe a typo in your HTML), Flask will throw a 400 Bad Request error and crash the page.

request.form.get('email'): This is the "safer" way.

The Benefit: If "email" is missing, it simply returns None instead of crashing your entire application.
    
"""


# The "Form Journey" Comparison
# Part of the ProcessManual HTML Method (What we did today)Flask-WTF Method (The automated way)
# ValidationYou have to write if statements to check if the field is empty.
# You add validators=[DataRequired()] in the Class.
# SecurityYou have to manually manage security tokens.{{ form.csrf_token }} handles it automatically.
# Request Handlingif request.method == "POST":
# if form.validate_on_submit():Data Retrievalrequest.form["book_name"]form.book_name.data