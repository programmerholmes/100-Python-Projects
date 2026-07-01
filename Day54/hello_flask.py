from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return ("<h1 style='text-align: center'>Hello, World!</h1>"
            "<p>Here you go, this is a paragraph now!</p>"
            "<img src='https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmYxMHBwcnQxdWdrNG8zeW80azVzMzJpc2phNXRsNWhwbG9waDRvYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Df0JB6yixeNqg/giphy.gif' width=400>")

def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper

def make_underlined(function):
    def wrapper():
        return "<u>" + function() + "</u>"
    return wrapper

@app.route('/bye')
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye"

@app.route('/<path:name>/<int:number>/<luck>/<another_name>')
def greet(name, number, luck, another_name):
    return f"Hello {name}, you are {number} years old!, I wish you {luck} luck,....{another_name}"


if __name__ == '__main__':
    app.run(debug=True)