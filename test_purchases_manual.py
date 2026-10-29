import sqlite3

from database import get_connection
from purchase_manager import PurchaseManager


manager = PurchaseManager()


def test_purchase_management():
    connection = get_connection()

    try:
        supplier = connection.execute(
            """
            SELECT supplier_id
            FROM suppliers
            WHERE supplier_id = ?
            """,
            ("SUP101",)
        ).fetchone()

        product = connection.execute(
            """
            SELECT product_id
            FROM products
            WHERE product_id = ?
            """,
            ("P101",)
        ).fetchone()

        if supplier is None:
            raise ValueError("Run the supplier test first.")

        if product is None:
            raise ValueError("Run the product test first.")

    finally:
        connection.close()

    print("\n--- STOCK BEFORE PURCHASE ---")
    show_stock("P101")

    print("\n--- CREATE PURCHASE ---")

    purchase_id = manager.create_purchase(
        supplier_id="SUP101",
        items=[
            {"product_id": "P101", "quantity": 10}
        ]
    )

    if purchase_id is not None:
        print("\n--- STOCK AFTER PURCHASE ---")
        show_stock("P101")

        print("\n--- PURCHASE HISTORY ---")
        manager.display_purchases()

        print("\n--- PURCHASE DETAILS ---")
        manager.display_purchase_details(purchase_id)


def show_stock(product_id):
    connection = get_connection()

    try:
        product = connection.execute(
            """
            SELECT name, quantity
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        ).fetchone()

        if product:
            print(f"Product: {product['name']}")
            print(f"Available Stock: {product['quantity']}")

    finally:
        connection.close()


if __name__ == "__main__":
    test_purchase_management()