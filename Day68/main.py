from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String


app = Flask(__name__)

class Base(DeclarativeBase):
    pass


app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)
    #return User.get(user_id)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
#Line below only required once, when creating DB. 
#with app.app_context():
   # db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "POST":

        email = request.form.get('email')
        # Check if user already exists
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
                                                                # these lines are only here, so we can flash.
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hashed_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method = 'pbkdf2:sha256',
            salt_length = 8
        )

        new_user = User(
            name = request.form.get('name'),
            email = request.form.get('email'),
            #password = request.form.get('password'),
            password = hashed_and_salted_password,
        )
        print(new_user.password)
        db.session.add(new_user)
        db.session.commit()

        #flash("Account created successfully! Please log in.", "success")
        login_user(new_user)
        #return redirect(url_for('login'))
        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = db.session.execute(db.select(User).where(User.email == email)).scalar()

        if user and check_password_hash(user.password, password):
            login_user(user)                                       # so flask doesn't forget after you go to a new page
            return redirect(url_for("secrets"))
        else:
            flash("Invalid credentials, try again.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
def download():
    return send_from_directory('static', path="files/cheat_sheet.pdf")



if __name__ == "__main__":
    app.run(debug=True)
