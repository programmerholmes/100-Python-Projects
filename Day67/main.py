from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Text
from datetime import date


## Delete this code:
# import requests
# posts = requests.get("https://json.extendsclass.com/bin/YOUR_JSON_BIN_ID").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOUR_SECRET_KEY_HERE'
ckeditor = CKEditor(app)
app.config['CKEDITOR_CDN_URL'] = "https://cdn.ckeditor.com/4.22.1/standard/ckeditor.js"
Bootstrap(app)

class Base(DeclarativeBase):
    pass

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    # Use CKEditorField for the big body section!
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")



@app.route('/')
def get_all_posts():
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts)



# This is how you would do it if you wanted to get it from the json API
# @app.route("/post/<int:index>")
# def show_post(index):
#     requested_post = None
#     for blog_post in posts:
#         if blog_post["id"] == index:
#             requested_post = blog_post
#     return render_template("post.html", post=requested_post)

# This is how it's done in the database
@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    return render_template("post.html", post=requested_post)


@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title = form.title.data,
            subtitle = form.subtitle.data,
            body = form.body.data,
            img_url = form.img_url.data,
            author = form.author.data,
            date = date.today().strftime("%B %d, %Y")
        )

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))

    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>")
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@app.route("/delete/<post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)






"""
Let's just suppose if i got this project and there was no entry in the database, and our data was still in the
json file, and we had to shift it from the json manually, and throw it in our database, then in that case we
would have to do this, which is not manual, but the idea is that we weren't given a database that had all the 
post already inserted in it for us to work around with 
This is a great "industry secret" to learn! In the professional world, 
we call this an ETL process (Extract, Transform, Load).

Imagine you are working for a company that is moving its old blog from a platform 
like WordPress or a custom JSON file over to a new internal system. 
You wouldn't want to copy-paste 500 articles by hand. You'd write a script to do it in seconds.

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ... (Standard Flask & SQLAlchemy Setup) ...

def migrate_data():
    # 1. EXTRACT: Get the data from the old API
    response = requests.get("https://api.npoint.io/your_old_json_endpoint")
    old_posts = response.json()

    # 2. TRANSFORM & LOAD: Loop through the JSON and turn them into Database Objects
    for post in old_posts:
        new_post = BlogPost(
            title=post["title"],
            subtitle=post["subtitle"],
            date=post["date"],
            body=post["body"],
            author=post["author"],
            img_url=post["img_url"]
        )
        # Add to the session
        db.session.add(new_post)
    
    # 3. COMMIT: Save everything to the database at once
    db.session.commit()
    print("Migration successful! All posts moved from API to Database.")

# You would run this function once, then delete it or comment it out!



But this wasn't needed just because our database already had all the data stored inside it, that we 
initially had in the json API
"""




"""
THE EDIT ROUTE LOGIC CHEAT SHEET:


first of all we have post.title vs post.title.data, is the difference because .data is only 
used to receive the information just written into the form and submitted, while the other one 
was retrieved from the database so we used only post.title, and even if we did use .data there 
for the prefilled, it would've been empty because there wasn't any data entered in the first place, 
right? Secondly, one has comma separated entries while the other doesn't, 
which would mean the same thing one is from the db and other is the form, and i 
notice over here we don't have the BlogPost written after the validate on submit, is 
it because we have already stored that information in the get_or_404, that's why it's not needed. 
third, post_id=post.id we could also write post_id=post_id, and it would be the exact same thing right ? 
And lastly the session.add isn't there because we aren't adding anything new just updating it, it's like PATCH, 
so we can link this with our second point of why we don't need to 
write BlogPost either and also session.add isn't needed


1. PRE-FILLING: We pass existing 'post' data into the Form class (e.g., title=post.title). 
   At this stage, the form's '.data' is empty until it receives these values.
2. ASSIGNMENT vs. CREATION: We don't call 'BlogPost()' again because we aren't creating 
   a new house; we are painting the walls of an existing one (post.title = form.title.data).
3. TARGETING: We use the object retrieved from 'get_or_404'. Because SQLAlchemy is 
   already "watching" this object, we don't need 'db.session.add()'.
4. COMMIT: SQLAlchemy detects the changes to the watched object and performs a SQL 'UPDATE' 
   (like a PATCH) instead of a SQL 'INSERT' when we call 'db.session.commit()'.
5. REUSE: We pass 'is_edit=True' to the template to toggle UI elements (like changing 
   the heading from 'New Post' to 'Edit Post') while using the same 'make-post.html' file.
   
   post_id=post.id vs post_id=post_id
Yes, they are mathematically identical in this context, but there is a tiny "best practice" reason to use post.id.

post_id is just a local variable (an integer) passed into the function.

post.id is the actual ID attribute of the database object we just retrieved.

Usually, developers use post.id because it guarantees that you are linking to the ID of the object you 
actually just manipulated. But if you wrote post_id=post_id, the code would work exactly the same!
"""