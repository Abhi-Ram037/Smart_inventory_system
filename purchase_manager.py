import sqlite3
from datetime import datetime
from decimal import Decimal, InvalidOperation

from database import get_connection


class PurchaseManager:

    def create_purchase(self, supplier_id, items):
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")

        if not isinstance(items, list) or not items:
            raise ValueError("Purchase must contain at least one product.")

        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            supplier = connection.execute(
                """
                SELECT supplier_id
                FROM suppliers
                WHERE supplier_id = ?
                """,
                (supplier_id.strip(),)
            ).fetchone()

            if supplier is None:
                raise ValueError("Supplier does not exist.")

            total_amount = Decimal("0.00")
            purchase_items = []

            for item in items:
                if not isinstance(item, dict):
                    raise ValueError("Each purchase item must be a dictionary.")

                product_id = item.get("product_id")
                quantity = item.get("quantity")

                if not isinstance(product_id, str) or not product_id.strip():
                    raise ValueError("Product ID cannot be empty.")

                if (
                    not isinstance(quantity, int)
                    or isinstance(quantity, bool)
                    or quantity <= 0
                ):
                    raise ValueError("Quantity must be a positive integer.")

                product = connection.execute(
                    """
                    SELECT product_id, purchase_price
                    FROM products
                    WHERE product_id = ?
                    """,
                    (product_id.strip(),)
                ).fetchone()

                if product is None:
                    raise ValueError(
                        f"Product {product_id} does not exist."
                    )

                price = Decimal(str(product["purchase_price"]))

                if not price.is_finite() or price < 0:
                    raise ValueError("Invalid product purchase price.")

                subtotal = price * quantity
                total_amount += subtotal

                purchase_items.append({
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "purchase_price": price,
                    "subtotal": subtotal
                })

            purchase_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor = connection.execute(
                """
                INSERT INTO purchases (
                    supplier_id,
                    purchase_date,
                    total_amount
                )
                VALUES (?, ?, ?)
                """,
                (
                    supplier_id.strip(),
                    purchase_date,
                    str(total_amount)
                )
            )

            purchase_id = cursor.lastrowid

            for item in purchase_items:
                connection.execute(
                    """
                    INSERT INTO purchase_items (
                        purchase_id,
                        product_id,
                        quantity,
                        purchase_price,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        purchase_id,
                        item["product_id"],
                        item["quantity"],
                        str(item["purchase_price"]),
                        str(item["subtotal"])
                    )
                )

                connection.execute(
                    """
                    UPDATE products
                    SET quantity = quantity + ?
                    WHERE product_id = ?
                    """,
                    (
                        item["quantity"],
                        item["product_id"]
                    )
                )

            connection.commit()

            print("\nPurchase completed successfully!")
            print(f"Purchase ID: {purchase_id}")
            print(f"Supplier ID: {supplier_id}")
            print(f"Purchase Date: {purchase_date}")
            print(f"Total Purchase Amount: Rs. {total_amount:.2f}")

            return purchase_id

        except (ValueError, InvalidOperation) as error:
            connection.rollback()
            print(f"Purchase failed: {error}")
            return None

        except sqlite3.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return None

        finally:
            connection.close()

    def display_purchases(self):
        connection = get_connection()

        try:
            purchases = connection.execute(
                """
                SELECT
                    p.purchase_id,
                    p.supplier_id,
                    s.name AS supplier_name,
                    p.purchase_date,
                    p.total_amount
                FROM purchases p
                JOIN suppliers s
                    ON p.supplier_id = s.supplier_id
                ORDER BY p.purchase_id DESC
                """
            ).fetchall()

            if not purchases:
                print("No purchases found.")
                return

            print("\n========== PURCHASE HISTORY ==========")

            for purchase in purchases:
                print(
                    f"Purchase ID: {purchase['purchase_id']} | "
                    f"Supplier: {purchase['supplier_name']} | "
                    f"Date: {purchase['purchase_date']} | "
                    f"Total: Rs. "
                    f"{Decimal(str(purchase['total_amount'])):.2f}"
                )

        except sqlite3.Error as error:
            print(f"Unable to display purchases: {error}")

        finally:
            connection.close()

    def display_purchase_details(self, purchase_id):
        connection = get_connection()

        try:
            purchase = connection.execute(
                """
                SELECT
                    p.purchase_id,
                    p.supplier_id,
                    s.name AS supplier_name,
                    p.purchase_date,
                    p.total_amount
                FROM purchases p
                JOIN suppliers s
                    ON p.supplier_id = s.supplier_id
                WHERE p.purchase_id = ?
                """,
                (purchase_id,)
            ).fetchone()

            if purchase is None:
                print("Purchase not found.")
                return

            items = connection.execute(
                """
                SELECT
                    pi.product_id,
                    pr.name AS product_name,
                    pi.quantity,
                    pi.purchase_price,
                    pi.subtotal
                FROM purchase_items pi
                JOIN products pr
                    ON pi.product_id = pr.product_id
                WHERE pi.purchase_id = ?
                """,
                (purchase_id,)
            ).fetchall()

            print("\n========== PURCHASE DETAILS ==========")
            print(f"Purchase ID: {purchase['purchase_id']}")
            print(f"Supplier: {purchase['supplier_name']}")
            print(f"Date: {purchase['purchase_date']}")

            for item in items:
                print(
                    f"Product: {item['product_name']} | "
                    f"ID: {item['product_id']} | "
                    f"Quantity: {item['quantity']} | "
                    f"Unit Price: Rs. "
                    f"{Decimal(str(item['purchase_price'])):.2f} | "
                    f"Subtotal: Rs. "
                    f"{Decimal(str(item['subtotal'])):.2f}"
                )

            print(
                f"Total: Rs. "
                f"{Decimal(str(purchase['total_amount'])):.2f}"
            )

        except sqlite3.Error as error:
            print(f"Unable to retrieve purchase details: {error}")

        finally:
            connection.close()