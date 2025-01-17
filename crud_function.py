import sqlite3

def initiate_db():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Products")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL,
        image TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance TEXT NOT NULL
        )
        """)
    conn.commit()
    conn.close()

def add_user(username, email, age):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (username, email, age, 1000))
    conn.commit()
    conn.close()

def is_included(username):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    user_exists = cursor.fetchone() is not None
    conn.close()
    return user_exists

def get_all_products():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    conn.close()
    return products


def insert_products():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    for i in range(1, 5):
        cursor.execute(
            "INSERT INTO Products(id, title, description, price, image) VALUES (?,?,?,?, ?)",
                       (i, f"Продукт {i}", f"Описание {i}", i * 100, f"{i}.jpg")
        )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initiate_db()
    insert_products()
