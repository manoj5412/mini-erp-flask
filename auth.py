import sqlite3

def connect():
    return sqlite3.connect("erp.db")

def register_admin():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    if cursor.fetchone():
        conn.close()
        return  # Admin already exists

    print("=== Create Admin Account ===")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()
    print("✅ Admin account created successfully!")

def login():
    conn = connect()
    cursor = conn.cursor()

    print("\n=== LOGIN ===")
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        print("✅ Login successful!")
        return True
    else:
        print("❌ Invalid credentials!")
        return False