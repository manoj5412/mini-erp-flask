import sqlite3

def connect():
    return sqlite3.connect("erp.db")

def add_supplier():
    name = input("Enter supplier name: ")
    contact = input("Enter supplier contact: ")

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO suppliers (name, contact) VALUES (?, ?)",
        (name, contact)
    )

    conn.commit()
    conn.close()

    print("✅ Supplier added successfully!")

def view_suppliers():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM suppliers")
    suppliers = cursor.fetchall()

    print("\n======= SUPPLIER LIST =======")
    print("ID | Name | Contact")
    print("-------------------------------")

    for supplier in suppliers:
        print(f"{supplier[0]} | {supplier[1]} | {supplier[2]}")

    conn.close()