import sqlite3
from decimal import Decimal
from database import get_connection


class Inventory:

    def display_low_stock(self):
        connection = get_connection()

        try:
            products = connection.execute("""
                SELECT product_id, name, category, quantity, minimum_stock
                FROM products
                WHERE quantity <= minimum_stock
                ORDER BY quantity ASC
            """).fetchall()

            print("\n========== LOW STOCK REPORT ==========")

            if not products:
                print("No low-stock products found.")
                return

            for product in products:
                print(
                    f"ID: {product['product_id']} | "
                    f"Name: {product['name']} | "
                    f"Stock: {product['quantity']} | "
                    f"Minimum Stock: {product['minimum_stock']}"
                )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()

    def display_out_of_stock(self):
        connection = get_connection()

        try:
            products = connection.execute("""
                SELECT product_id, name, category, quantity
                FROM products
                WHERE quantity = 0
                ORDER BY name
            """).fetchall()

            print("\n========== OUT OF STOCK REPORT ==========")

            if not products:
                print("No out-of-stock products found.")
                return

            for product in products:
                print(
                    f"ID: {product['product_id']} | "
                    f"Name: {product['name']} | "
                    f"Category: {product['category']} | "
                    f"Stock: {product['quantity']}"
                )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()

    def display_inventory_value(self):
        connection = get_connection()

        try:
            result = connection.execute("""
                SELECT
                    COUNT(*) AS total_products,
                    COALESCE(SUM(quantity), 0) AS total_units,
                    COALESCE(
                        SUM(quantity * purchase_price), 0
                    ) AS inventory_value
                FROM products
            """).fetchone()

            inventory_value = Decimal(str(result["inventory_value"]))

            print("\n========== INVENTORY VALUATION ==========")
            print(f"Total Product Types: {result['total_products']}")
            print(f"Total Units in Stock: {result['total_units']}")
            print(f"Inventory Value: Rs. {inventory_value:.2f}")

        except (sqlite3.Error, ArithmeticError, ValueError) as error:
            print(f"Error calculating inventory value: {error}")

        finally:
            connection.close()

    def display_top_selling_products(self):
        connection = get_connection()

        try:
            products = connection.execute("""
                SELECT
                    p.product_id,
                    p.name,
                    COALESCE(SUM(si.quantity), 0) AS total_sold
                FROM products p
                INNER JOIN sale_items si
                    ON p.product_id = si.product_id
                GROUP BY p.product_id, p.name
                ORDER BY total_sold DESC, p.name ASC
                LIMIT 5
            """).fetchall()

            print("\n========== TOP 5 BEST-SELLING PRODUCTS ==========")

            if not products:
                print("No sales records found.")
                return

            for rank, product in enumerate(products, start=1):
                print(
                    f"{rank}. {product['name']} | "
                    f"Product ID: {product['product_id']} | "
                    f"Quantity Sold: {product['total_sold']}"
                )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()

    def display_stock_movement_history(self):
        connection = get_connection()

        try:
            movements = connection.execute("""
                SELECT
                    p.purchase_date AS movement_date,
                    'PURCHASE' AS movement_type,
                    pr.product_id,
                    pr.name,
                    pi.quantity AS quantity_changed
                FROM purchase_items pi
                INNER JOIN purchases p
                    ON pi.purchase_id = p.purchase_id
                INNER JOIN products pr
                    ON pi.product_id = pr.product_id

                UNION ALL

                SELECT
                    s.sale_date AS movement_date,
                    'SALE' AS movement_type,
                    pr.product_id,
                    pr.name,
                    -si.quantity AS quantity_changed
                FROM sale_items si
                INNER JOIN sales s
                    ON si.sale_id = s.sale_id
                INNER JOIN products pr
                    ON si.product_id = pr.product_id

                ORDER BY movement_date DESC
            """).fetchall()

            print("\n========== STOCK MOVEMENT HISTORY ==========")

            if not movements:
                print("No stock movements found.")
                return

            for movement in movements:
                print(
                    f"Date: {movement['movement_date']} | "
                    f"Type: {movement['movement_type']} | "
                    f"Product: {movement['name']} | "
                    f"ID: {movement['product_id']} | "
                    f"Stock Change: {movement['quantity_changed']:+}"
                )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()