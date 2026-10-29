from decimal import Decimal

from database import get_connection
from sales_manager import SalesManager


manager = SalesManager()


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


def test_sales_management():
    print("\n--- STOCK BEFORE SALE ---")
    show_stock("P101")

    print("\n--- CREATE SALE ---")

    sale_id = manager.create_sale(
        items=[
            {"product_id": "P101", "quantity": 2}
        ],
        discount=Decimal("50.00"),
        tax_rate=Decimal("0.00")
    )

    if sale_id is not None:
        print("\n--- STOCK AFTER SALE ---")
        show_stock("P101")

        connection = get_connection()

        try:
            sale = connection.execute(
                """
                SELECT invoice_number
                FROM sales
                WHERE sale_id = ?
                """,
                (sale_id,)
            ).fetchone()

            invoice_number = sale["invoice_number"]

        finally:
            connection.close()

        print("\n--- SALES HISTORY ---")
        manager.display_sales()

        print("\n--- INVOICE DETAILS ---")
        manager.display_invoice(invoice_number)


if __name__ == "__main__":
    test_sales_management()