from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session

def check_login(username, password):
    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if check_login(username, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Credentials ❌"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))



@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        supplier_id = request.form["supplier_id"]

        conn = sqlite3.connect("erp.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, price, quantity, supplier_id) VALUES (?, ?, ?, ?)",
            (name, price, quantity, supplier_id)
        )
        conn.commit()
        conn.close()

        return "Product Added Successfully ✅"

    return render_template("add_product.html")

@app.route("/view_products")
def view_products():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()

    return render_template("view_products.html", products=products)
@app.route("/add_supplier", methods=["GET", "POST"])
def add_supplier():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form["name"]
        contact = request.form["contact"]

        conn = sqlite3.connect("erp.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO suppliers (name, contact) VALUES (?, ?)",
            (name, contact)
        )
        conn.commit()
        conn.close()

        return "Supplier Added Successfully ✅"

    return render_template("add_supplier.html")


@app.route("/view_suppliers")
def view_suppliers():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("erp.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()
    conn.close()

    return render_template("view_suppliers.html", suppliers=suppliers)

if __name__ == "__main__":
    app.run(debug=True)