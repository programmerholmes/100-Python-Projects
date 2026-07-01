# Reflection

This was the biggest project so far: a real online shop, which meant tying
together everything from the Flask chapters — a database, user accounts, sessions,
forms, and an external payment API — into one coherent app instead of a single
feature.

I approached it by building outward from the data. First the models (`User`,
`Product`, `Order`, `OrderItem`) and a seeded catalogue, then the shop and
product pages, then the cart, then authentication, and finally checkout. Keeping
each layer working before starting the next one meant I always had something I
could run and click through, rather than a big pile of half-finished parts.

The cart was easier than I expected once I decided to keep it in the **session**
as a simple `{product_id: quantity}` dictionary — no extra tables, and it just
follows the browser around. Authentication was familiar from earlier days
(Flask-Login + hashed passwords). The part that needed the most care was
**checkout**: creating a Stripe Checkout Session with line-items built from the
cart, sending the user to Stripe's hosted page, and then turning the cart into a
saved `Order` *only after* payment succeeds — including guarding against
double-creating the order if the success page is refreshed.

A decision I'm happy with was making Stripe **optional**: the app reads the key
from a `.env` file and, if there isn't one, falls back to a "demo checkout". That
means the whole thing runs for anyone immediately, while still supporting real
(test-mode) card payments when a key is added — and it kept my secret key out of
the code entirely.

My biggest takeaway is that a larger app is really just small, well-understood
pieces wired together carefully — and that the interesting bugs live at the
*seams* (payment → order, cart → session, login → checkout), especially around
the "what if the user refreshes / isn't logged in / pays halfway" cases.

If I did it again I'd add stock levels, order confirmation emails, and a Stripe
**webhook** so the order is recorded from Stripe's event rather than the browser
redirect (more reliable if the customer closes the tab after paying).
