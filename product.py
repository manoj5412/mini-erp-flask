import sqlite3

def connect():
    return sqlite3.connect("erp.db")

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter product price: "))
    quantity = int(input("Enter product quantity: "))
    supplier_id = int(input("Enter supplier ID: "))

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, quantity, supplier_id) VALUES (?, ?, ?, ?)",
        (name, price, quantity, supplier_id)
    )

    conn.commit()
    conn.close()

    print("✅ Product added successfully!")

def view_products():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT p.id, p.name, p.price, p.quantity, s.name
    FROM products p
    LEFT JOIN suppliers s ON p.supplier_id = s.id
    """)

    products = cursor.fetchall()

    print("\n======= PRODUCT LIST =======")
    print("ID | Name | Price | Quantity | Supplier")
    print("--------------------------------------------------")

    for product in products:
        print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]} | {product[4]}")

    conn.close()

def low_stock_alert():
    conn = connect()
    cursor = conn.cursor()

    threshold = 10  # minimum stock level

    cursor.execute("SELECT * FROM products WHERE quantity < ?", (threshold,))
    low_stock_products = cursor.fetchall()

    print("\n======= LOW STOCK ALERT =======")
    print("ID | Name | Price | Quantity")
    print("--------------------------------")

    if not low_stock_products:
        print("✅ All products have sufficient stock.")
    else:
        for product in low_stock_products:
            print(f"{product[0]} | {product[1]} | {product[2]} | {product[3]}")

    conn.close()

import csv

def export_inventory_report():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    with open("inventory_report.csv", mode="w", newline="") as file:
        writer = csv.writer(file)

        # Header row
        writer.writerow(["ID", "Name", "Price", "Quantity"])

        # Data rows
        for product in products:
            writer.writerow(product)

    conn.close()

    print("✅ Inventory report exported successfully as inventory_report.csv")