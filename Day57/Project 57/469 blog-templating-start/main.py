from flask import Flask, render_template
import requests
from post import Post


posts = requests.get("https://api.npoint.io/YOUR_JSON_BIN_ID").json()
post_objects = []

for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


app = Flask(__name__)

## without post class
# @app.route('/')
# def home():
#     blog_url = "https://api.npoint.io/YOUR_JSON_BIN_ID"
#     response = requests.get(blog_url)
#     all_posts = response.json()
#     return render_template("index.html", posts=all_posts)

## without post Class
# @app.route('/post/<int:blog_id>')
# def show_post(blog_id):
#     print(blog_id)
#     blog_url = "https://api.npoint.io/YOUR_JSON_BIN_ID"
#     response = requests.get(blog_url)
#     all_posts = response.json()
#     post_title = all_posts[blog_id-1]['title']
#     print(post_title)
#     post_body= all_posts[blog_id-1]['body']
#     return render_template("post.html", title=post_title,body=post_body)

#with post Class
@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)

@app.route("/post/<int:blog_id>")
def show_post(blog_id):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == blog_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
