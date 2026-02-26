import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect("erp.db")

def update_stock():
    product_id = int(input("Enter Product ID: "))
    transaction_type = input("Enter type (IN/OUT): ").upper()
    quantity = int(input("Enter quantity: "))

    conn = connect()
    cursor = conn.cursor()

    # Get current stock
    cursor.execute("SELECT quantity FROM products WHERE id = ?", (product_id,))
    result = cursor.fetchone()

    if result is None:
        print("❌ Product not found!")
        conn.close()
        return

    current_quantity = result[0]

    if transaction_type == "IN":
        new_quantity = current_quantity + quantity
    elif transaction_type == "OUT":
        if quantity > current_quantity:
            print("❌ Not enough stock!")
            conn.close()
            return
        new_quantity = current_quantity - quantity
    else:
        print("❌ Invalid transaction type!")
        conn.close()
        return

    # Update product table
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?",
                   (new_quantity, product_id))

    # Record transaction
    cursor.execute(
        "INSERT INTO transactions (product_id, type, quantity, date) VALUES (?, ?, ?, ?)",
        (product_id, transaction_type, quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

    print("✅ Stock updated successfully!")
def view_transactions():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT t.id, p.name, t.type, t.quantity, t.date
    FROM transactions t
    JOIN products p ON t.product_id = p.id
    ORDER BY t.date DESC
    """)

    records = cursor.fetchall()

    print("\n======= TRANSACTION HISTORY =======")
    print("ID | Product | Type | Quantity | Date")
    print("--------------------------------------------------")

    for record in records:
        print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]}")

    conn.close()