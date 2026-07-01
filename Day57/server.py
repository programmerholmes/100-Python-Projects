from flask import Flask, render_template
import random
from datetime import datetime
import requests


app = Flask(__name__)


@app.route('/')
def home():
    random_number = random.randint(1, 10)
    current_year = datetime.now().year
    return render_template("index.html", num=random_number, year=current_year)


@app.route('/guess/<name>')
def game(name):
    age_response = requests.get(f"https://api.agify.io?name={name}")
    age = age_response.json()["age"]

    gender_url = f"https://api.genderize.io?name={name}"
    gender_response = requests.get(url=gender_url)                                       # Two different ways, for fun.
    gender_data = gender_response.json()
    gender = gender_data["gender"]

    return render_template("guess.html", person_name= name, person_age=age, person_gender=gender)


@app.route('/blog/<num>/<num2>')
def get_blog(num, num2):
    print(num)
    blog_url = "https://api.npoint.io/YOUR_JSON_BIN_ID"
    response = requests.get(blog_url)
    blog_data = response.json()
    print(blog_data)
    return render_template("blog.html", posts=blog_data)

if __name__ == "__main__":
    app.run(debug=True)