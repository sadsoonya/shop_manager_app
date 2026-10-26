import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "shop.db"


class ShopDatabase:
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                quantity INTEGER NOT NULL CHECK(quantity >= 0)
            )
        """)

        self.connection.commit()

    def get_products(self, search=""):
        cursor = self.connection.cursor()

        if search.strip():
            cursor.execute("""
                SELECT id, name, price, quantity
                FROM products
                WHERE name LIKE ?
                ORDER BY id DESC
            """, (f"%{search.strip()}%",))
        else:
            cursor.execute("""
                SELECT id, name, price, quantity
                FROM products
                ORDER BY id DESC
            """)

        return cursor.fetchall()

    def add_product(self, name, price, quantity):
        self.connection.execute("""
            INSERT INTO products (name, price, quantity)
            VALUES (?, ?, ?)
        """, (name, price, quantity))

        self.connection.commit()

    def update_price(self, product_id, price):
        cursor = self.connection.execute("""
            UPDATE products
            SET price = ?
            WHERE id = ?
        """, (price, product_id))

        self.connection.commit()
        return cursor.rowcount > 0

    def update_quantity(self, product_id, quantity):
        cursor = self.connection.execute("""
            UPDATE products
            SET quantity = ?
            WHERE id = ?
        """, (quantity, product_id))

        self.connection.commit()
        return cursor.rowcount > 0

    def delete_product(self, product_id):
        cursor = self.connection.execute("""
            DELETE FROM products
            WHERE id = ?
        """, (product_id,))

        self.connection.commit()
        return cursor.rowcount > 0

    def get_statistics(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS product_count,
                COALESCE(SUM(quantity), 0) AS total_quantity,
                COALESCE(SUM(price * quantity), 0) AS total_value
            FROM products
        """)

        return cursor.fetchone()

    def close(self):
        self.connection.close()