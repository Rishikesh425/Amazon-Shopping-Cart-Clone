from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
from AmazonCart2 import categories, get_items, bank_accounts

app = Flask(__name__)
app.secret_key = "shopping_secret_key"

# ─────────────────────────────────────────────
# PRODUCT DATA & BANK ACCOUNTS - Imported from AmazonCart2.py
# ─────────────────────────────────────────────

# ─────────────────────────────────────────────
# Product stock — initialised once at startup
# ─────────────────────────────────────────────
product_stock = {}

def initialize_stock():
    for category in categories:
        for subcategory in categories[category]:
            for brand in categories[category][subcategory]:
                for model in categories[category][subcategory][brand]:
                    details = categories[category][subcategory][brand][model]
                    if isinstance(details, dict) and "price" in details:
                        name = f"{brand} {model}"
                        product_stock[name] = 10
                    elif isinstance(details, dict):
                        for submodel in details:
                            name = f"{brand} {submodel}"
                            product_stock[name] = 10

initialize_stock()

# ─────────────────────────────────────────────
# Helper: build flat product list for a subcategory
# ─────────────────────────────────────────────
def get_items(category, subcategory):
    items = categories[category][subcategory]
    product_list = []
    for brand, models in items.items():
        for model, details in models.items():
            # Case 1: direct product
            if isinstance(details, dict) and "price" in details and "specs" in details:
                name  = f"{brand} {model}"
                price = details["price"]
                specs = details["specs"]
                product_list.append({"name": name, "price": price, "specs": specs})
            # Case 2: nested product (e.g. Clothes > Men > Shirts)
            elif isinstance(details, dict):
                for submodel, info in details.items():
                    if isinstance(info, dict) and "price" in info and "specs" in info:
                        name  = f"{brand} {submodel}"
                        price = info["price"]
                        specs = info["specs"]
                        product_list.append({"name": name, "price": price, "specs": specs})
    return product_list

# ─────────────────────────────────────────────
# Session cart helpers
# ─────────────────────────────────────────────
def get_cart():
    if "cart" not in session:
        session["cart"] = []   # list of {name, price, qty}
    return session["cart"]

def save_cart(cart):
    session["cart"] = cart
    session.modified = True

def cart_total(cart):
    return sum(item["price"] * item["qty"] for item in cart)

# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.route("/")
def index():
    cats = list(categories.keys())
    cart = get_cart()
    return render_template("index.html", categories=cats, cart_count=len(cart))


@app.route("/category/<category>")
def subcategory_page(category):
    if category not in categories:
        return redirect(url_for("index"))
    subs = list(categories[category].keys())
    cart = get_cart()
    return render_template("subcategory.html", category=category,
                           subcategories=subs, cart_count=len(cart))


@app.route("/category/<category>/<subcategory>")
def items_page(category, subcategory):
    if category not in categories or subcategory not in categories[category]:
        return redirect(url_for("index"))
    items = get_items(category, subcategory)
    cart  = get_cart()
    message = request.args.get("message", "")
    return render_template("items.html", category=category,
                           subcategory=subcategory, items=items,
                           product_stock=product_stock,
                           cart_count=len(cart), message=message)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    name     = request.form.get("name")
    price    = int(request.form.get("price"))
    qty      = int(request.form.get("qty", 1))
    category    = request.form.get("category")
    subcategory = request.form.get("subcategory")

    if qty <= 0:
        return redirect(url_for("items_page", category=category,
                                subcategory=subcategory,
                                message="Quantity must be positive."))

    stock = product_stock.get(name, 0)
    if qty > stock:
        return redirect(url_for("items_page", category=category,
                                subcategory=subcategory,
                                message=f"Not enough stock for {name}. Available: {stock}"))

    cart = get_cart()
    for item in cart:
        if item["name"] == name:
            item["qty"] += qty
            save_cart(cart)
            product_stock[name] -= qty
            return redirect(url_for("items_page", category=category,
                                    subcategory=subcategory,
                                    message=f"✅ {qty} x {name} added to cart."))

    cart.append({"name": name, "price": price, "qty": qty})
    save_cart(cart)
    product_stock[name] -= qty
    return redirect(url_for("items_page", category=category,
                            subcategory=subcategory,
                            message=f"✅ {qty} x {name} added to cart."))


@app.route("/cart")
def view_cart():
    cart    = get_cart()
    total   = cart_total(cart)
    message = request.args.get("message", "")
    return render_template("cart.html", cart=cart, total=total,
                           message=message, cart_count=len(cart))


@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    name       = request.form.get("name", "").strip()
    remove_qty = int(request.form.get("remove_qty", 0))

    cart = get_cart()
    for item in cart:
        if item["name"] == name:
            if remove_qty <= 0:
                return redirect(url_for("view_cart", message="Invalid quantity."))
            if remove_qty > item["qty"]:
                return redirect(url_for("view_cart",
                                        message="You cannot remove more than existing quantity."))
            item["qty"] -= remove_qty
            product_stock[name] = product_stock.get(name, 0) + remove_qty
            if item["qty"] == 0:
                cart.remove(item)
            save_cart(cart)
            return redirect(url_for("view_cart",
                                    message=f"✅ {remove_qty} x {name} removed from cart."))

    return redirect(url_for("view_cart", message="Product not found in cart."))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    cart  = get_cart()
    total = cart_total(cart)

    if not cart:
        return redirect(url_for("view_cart", message="Cart is empty."))

    if request.method == "POST":
        payment_method = request.form.get("payment_method")

        if payment_method == "cod":
            session["last_order"] = {
                "cart": list(cart),
                "total": total,
                "method": "Cash on Delivery",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            session["cart"] = []
            session.modified = True
            return redirect(url_for("order_success"))

        elif payment_method == "online":
            account_no = request.form.get("account_no", "").strip()
            if account_no not in bank_accounts:
                return render_template("checkout.html", cart=cart, total=total,
                                       cart_count=len(cart),
                                       error="Invalid bank account number.")
            account = bank_accounts[account_no]
            if account["balance"] < total:
                return render_template("checkout.html", cart=cart, total=total,
                                       cart_count=len(cart),
                                       error=f"Insufficient balance. Available: ₹{account['balance']}")
            bank_accounts[account_no]["balance"] -= total
            session["last_order"] = {
                "cart": list(cart),
                "total": total,
                "method": f"Online Payment (Account: {account_no}, Name: {account['name']})",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "remaining_balance": bank_accounts[account_no]["balance"]
            }
            session["cart"] = []
            session.modified = True
            return redirect(url_for("order_success"))

    return render_template("checkout.html", cart=cart, total=total,
                           cart_count=len(cart), error="")


@app.route("/order_success")
def order_success():
    order = session.get("last_order", {})
    return render_template("order_success.html", order=order, cart_count=0)


if __name__ == "__main__":
    app.run(debug=True)
