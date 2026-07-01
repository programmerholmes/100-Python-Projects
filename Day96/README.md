# Framed 🖼️ — a Flask eCommerce store

An online shop for art & photo prints, built with **Flask**. It has everything a
real store needs: a product catalogue, a working **cart**, user **accounts**, and
**checkout with card payments via Stripe**.

## Features

- 🛍️ Product catalogue stored in a **SQLite** database (seeded on first run).
- 🛒 A working **cart** — add, change quantity, remove — kept in your session.
- 👤 **Register / log in / log out** with securely hashed passwords (Flask-Login).
- 💳 **Checkout & card payment via Stripe Checkout** (test mode).
- 🧾 Orders are saved, with an **order-history** page.
- 🔒 Checkout requires an account; forms are CSRF-protected.

## Run it

```bash
pip install -r requirements.txt
python main.py
```

It opens **http://127.0.0.1:5000** automatically. Register an account, add some
prints to your cart, and check out.

## Payments (Stripe)

The app works out of the box: **without any Stripe key it uses a built-in "demo
checkout"** so you can complete the whole flow immediately.

To enable **real Stripe Checkout** (still test mode — no real money):

1. Make a free Stripe account and open **Developers → API keys** in *test mode*:
   <https://dashboard.stripe.com/test/apikeys>
2. Copy `.env.example` to `.env` and paste your **test secret key** (`sk_test_…`):
   ```
   STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxx
   FLASK_SECRET_KEY=any-random-string
   ```
3. Restart the app and check out. Use Stripe's **test card**:
   > **4242 4242 4242 4242** · any future expiry · any 3-digit CVC · any ZIP

Your secret key lives only in `.env` on your machine (it's git-ignored).

## How it works

- `main.py` holds the Flask app: the SQLAlchemy models (`User`, `Product`,
  `Order`, `OrderItem`), the cart (session-based), auth (Flask-Login + hashed
  passwords + WTForms), and checkout.
- **Checkout** builds Stripe line-items from the cart and creates a Stripe
  Checkout Session, redirecting to Stripe's hosted payment page; on success it
  saves the order and clears the cart. If no Stripe key is set, it creates the
  order directly (demo mode).
- Templates (`templates/`) use Jinja + Bootstrap 5; styling is in
  `static/style.css`. The database file is created under `instance/`.

## Files

```
main.py                app: models, cart, auth, checkout
templates/             base, shop, product, cart, login, register, orders, success
static/style.css       styling
.env.example           copy to .env and add your Stripe test key
requirements.txt       dependencies
reflection.md          project notes
```
