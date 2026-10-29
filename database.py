import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "inventory.db"


def get_connection():
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    connection = get_connection()

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                purchase_price NUMERIC NOT NULL
                    CHECK (purchase_price >= 0),
                selling_price NUMERIC NOT NULL
                    CHECK (selling_price >= 0),
                quantity INTEGER NOT NULL DEFAULT 0
                    CHECK (quantity >= 0),
                minimum_stock INTEGER NOT NULL DEFAULT 5
                    CHECK (minimum_stock >= 0)
            );

            CREATE TABLE IF NOT EXISTS suppliers (
                supplier_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS purchases (
                purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_id TEXT NOT NULL,
                purchase_date TEXT NOT NULL,
                total_amount NUMERIC NOT NULL
                    CHECK (total_amount >= 0),
                FOREIGN KEY (supplier_id)
                    REFERENCES suppliers(supplier_id)
            );

            CREATE TABLE IF NOT EXISTS purchase_items (
                purchase_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_id INTEGER NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                purchase_price NUMERIC NOT NULL
                    CHECK (purchase_price >= 0),
                subtotal NUMERIC NOT NULL CHECK (subtotal >= 0),
                FOREIGN KEY (purchase_id)
                    REFERENCES purchases(purchase_id),
                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            );

            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT NOT NULL UNIQUE,
                sale_date TEXT NOT NULL,
                subtotal NUMERIC NOT NULL CHECK (subtotal >= 0),
                discount NUMERIC NOT NULL DEFAULT 0
                    CHECK (discount >= 0),
                tax NUMERIC NOT NULL DEFAULT 0
                    CHECK (tax >= 0),
                final_amount NUMERIC NOT NULL
                    CHECK (final_amount >= 0)
            );

            CREATE TABLE IF NOT EXISTS sale_items (
                sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                selling_price NUMERIC NOT NULL
                    CHECK (selling_price >= 0),
                purchase_price NUMERIC NOT NULL
                    CHECK (purchase_price >= 0),
                subtotal NUMERIC NOT NULL CHECK (subtotal >= 0),
                FOREIGN KEY (sale_id)
                    REFERENCES sales(sale_id),
                FOREIGN KEY (product_id)
                    REFERENCES products(product_id)
            );

            CREATE INDEX IF NOT EXISTS idx_products_name
                ON products(name);

            CREATE INDEX IF NOT EXISTS idx_sales_date
                ON sales(sale_date);

            CREATE INDEX IF NOT EXISTS idx_purchases_date
                ON purchases(purchase_date);
        """)

        connection.commit()
        print("Database initialized successfully.")

    except sqlite3.Error:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()