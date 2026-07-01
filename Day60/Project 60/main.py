from flask import Flask, render_template, request
import requests
from post import Post
import smtplib



posts = requests.get("https://api.npoint.io/YOUR_JSON_BIN_ID").json()
post_objects = []

for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)


app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=post_objects)

@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/header")
def header():
    return render_template("header.html")



@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        print(name, "\n", email, "\n", phone, "\n", message)
        send_email(name, email, phone, message)
        return render_template("contact.html", msg_sent = True)
    return render_template("contact.html", msg_sent = False)



def send_email(name, email, phone, message):
    my_email = "YOUR_EMAIL@gmail.com"
    password = "YOUR_APP_PASSWORD"
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"


    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()                                                   # responsible for encrypting and securing connection
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="RECIPIENT_EMAIL@gmail.com", msg=email_message)




@app.route("/post/<int:blog_id>")
def show_post(blog_id):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == blog_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

if __name__ == "__main__":
    app.run(debug=True)
