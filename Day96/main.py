"""
Framed — a small eCommerce website (Flask).

An online shop for art & photo prints with everything a store needs:
  * a product catalogue (stored in a SQLite database, seeded on first run)
  * a working cart (add / update quantity / remove), kept in the session
  * user accounts: register, log in, log out (hashed passwords, Flask-Login)
  * checkout & real card payments via Stripe Checkout (test mode)
  * saved orders + an order-history page

Payments:
  Add your Stripe TEST secret key to a `.env` file (see `.env.example`) and
  checkout uses real Stripe Checkout with test cards. WITHOUT a key, the app
  falls back to a built-in "demo checkout" so the whole flow still works.

Run it:
    python main.py            # opens http://127.0.0.1:5000

Needs: flask, flask-sqlalchemy, flask-login, flask-wtf, wtforms,
       email_validator, stripe   (pip install -r requirements.txt)
"""

import os
import threading
import webbrowser
from datetime import datetime

import stripe
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Email, InputRequired, Length


# --- tiny .env loader (so we don't need an extra dependency) ---------------
def load_dotenv(path=".env"):
    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Stripe is used only if a secret key is configured; otherwise we demo-checkout.
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_ENABLED = stripe.api_key.startswith("sk_")


# ---------------------------------------------------------------------------
# Database models
# ---------------------------------------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    orders = db.relationship("Order", backref="user", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    price_cents = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400), nullable=False)

    @property
    def price(self):
        return self.price_cents / 100


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    total_cents = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="paid")
    stripe_session_id = db.Column(db.String(255), nullable=True)
    items = db.relationship("OrderItem", backref="order", lazy=True)

    @property
    def total(self):
        return self.total_cents / 100


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    image = db.Column(db.String(400), nullable=False)
    unit_price_cents = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    @property
    def subtotal(self):
        return self.unit_price_cents * self.quantity / 100


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ---------------------------------------------------------------------------
# Seed the catalogue on first run
# ---------------------------------------------------------------------------
SEED_PRINTS = [
    ("Misty Peaks", "A calm morning over layered mountain ridges.", 2900, "misty-peaks"),
    ("Golden Coast", "Warm sunset light along a quiet shoreline.", 3400, "golden-coast"),
    ("Urban Nights", "City lights and long exposures after dark.", 3900, "urban-nights"),
    ("Desert Dunes", "Soft curves of windswept desert sand.", 2600, "desert-dunes"),
    ("Forest Path", "A winding trail through tall green pines.", 2400, "forest-path"),
    ("Ocean Calm", "Minimalist blues where the sea meets the sky.", 3100, "ocean-calm"),
    ("Autumn Leaves", "Rich reds and golds of a fall canopy.", 2200, "autumn-leaves"),
    ("Aurora Sky", "Northern lights dancing over the tundra.", 4500, "aurora-sky"),
]


def seed_products():
    if Product.query.first():
        return
    for name, desc, cents, slug in SEED_PRINTS:
        db.session.add(Product(
            name=name, description=desc, price_cents=cents,
            image=f"https://picsum.photos/seed/{slug}/600/450",
        ))
    db.session.commit()


with app.app_context():
    db.create_all()
    seed_products()


# ---------------------------------------------------------------------------
# Cart helpers (the cart lives in the user's session as {product_id: quantity})
# ---------------------------------------------------------------------------
def get_cart():
    return session.get("cart", {})


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


def cart_items():
    """Return [{product, quantity, subtotal_cents}] for the current cart."""
    cart = get_cart()
    items = []
    if cart:
        products = Product.query.filter(Product.id.in_([int(i) for i in cart])).all()
        for p in products:
            qty = cart.get(str(p.id), 0)
            items.append({"product": p, "quantity": qty, "subtotal_cents": p.price_cents * qty})
    return items


def cart_total_cents():
    return sum(i["subtotal_cents"] for i in cart_items())


@app.context_processor
def inject_cart_count():
    return {"cart_count": sum(get_cart().values())}


# ---------------------------------------------------------------------------
# Forms
# ---------------------------------------------------------------------------
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), Length(max=80)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6)])
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log in")


# ---------------------------------------------------------------------------
# Shop + cart routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route("/product/<int:product_id>")
def product(product_id):
    return render_template("product.html", product=db.get_or_404(Product, product_id))


@app.route("/cart")
def cart():
    items = cart_items()
    return render_template("cart.html", items=items, total_cents=cart_total_cents())


@app.route("/cart/add/<int:product_id>", methods=["POST"])
def cart_add(product_id):
    db.get_or_404(Product, product_id)                 # 404 if it doesn't exist
    qty = max(1, int(request.form.get("quantity", 1)))
    cart = get_cart()
    cart[str(product_id)] = cart.get(str(product_id), 0) + qty
    save_cart(cart)
    flash("Added to cart.", "success")
    return redirect(request.form.get("next") or url_for("cart"))


@app.route("/cart/update", methods=["POST"])
def cart_update():
    cart = get_cart()
    for key, value in request.form.items():
        if key.startswith("qty_"):
            pid = key[4:]
            qty = int(value)
            if qty > 0:
                cart[pid] = qty
            else:
                cart.pop(pid, None)
    save_cart(cart)
    flash("Cart updated.", "success")
    return redirect(url_for("cart"))


@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def cart_remove(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    save_cart(cart)
    return redirect(url_for("cart"))


# ---------------------------------------------------------------------------
# Checkout + payment
# ---------------------------------------------------------------------------
@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    items = cart_items()
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart"))

    if STRIPE_ENABLED:
        line_items = [{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": i["product"].name, "images": [i["product"].image]},
                "unit_amount": i["product"].price_cents,
            },
            "quantity": i["quantity"],
        } for i in items]
        checkout_session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            customer_email=current_user.email,
            success_url=url_for("success", _external=True) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=url_for("cart", _external=True),
        )
        return redirect(checkout_session.url, code=303)

    # No Stripe key configured -> demo checkout (skips real payment).
    return redirect(url_for("success", demo="1"))


def create_order(stripe_session_id=None):
    """Turn the current cart into a saved Order for the logged-in user."""
    items = cart_items()
    order = Order(
        user_id=current_user.id,
        total_cents=cart_total_cents(),
        stripe_session_id=stripe_session_id,
        status="paid",
    )
    db.session.add(order)
    db.session.flush()
    for i in items:
        db.session.add(OrderItem(
            order_id=order.id, name=i["product"].name, image=i["product"].image,
            unit_price_cents=i["product"].price_cents, quantity=i["quantity"],
        ))
    db.session.commit()
    save_cart({})
    return order


@app.route("/success")
@login_required
def success():
    session_id = request.args.get("session_id")

    if STRIPE_ENABLED and session_id:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        if checkout_session.payment_status != "paid":
            flash("Payment was not completed.", "warning")
            return redirect(url_for("cart"))
        order = Order.query.filter_by(stripe_session_id=session_id).first()
        if order is None:               # don't double-create on refresh
            order = create_order(stripe_session_id=session_id)
    else:
        if not cart_items():
            return redirect(url_for("index"))
        order = create_order()

    return render_template("success.html", order=order, demo=not STRIPE_ENABLED)


@app.route("/orders")
@login_required
def orders():
    my_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template("orders.html", orders=my_orders)


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.lower()).first():
            flash("That email is already registered — please log in.", "warning")
            return redirect(url_for("login"))
        user = User(
            name=form.name.data,
            email=form.email.data.lower(),
            password=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"Welcome, {user.name}!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(request.args.get("next") or url_for("index"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("index"))


def _open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1.0, _open_browser).start()
    app.run(debug=True)
