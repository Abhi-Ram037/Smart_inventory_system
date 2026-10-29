import sqlite3
from decimal import Decimal, InvalidOperation

from database import get_connection
from models import Product


class ProductManager:

    def validate_product(self, product):
        if not product.product_id.strip():
            raise ValueError("Product ID cannot be empty.")

        if not product.name.strip():
            raise ValueError("Product name cannot be empty.")

        if not product.category.strip():
            raise ValueError("Category cannot be empty.")

        try:
            purchase_price = Decimal(str(product.purchase_price))
            selling_price = Decimal(str(product.selling_price))
        except (InvalidOperation, ValueError):
            raise ValueError("Prices must be valid numbers.")

        if not purchase_price.is_finite() or not selling_price.is_finite():
            raise ValueError("Prices must be finite numbers.")

        if purchase_price < 0 or selling_price < 0:
            raise ValueError("Prices cannot be negative.")

        if not isinstance(product.quantity, int) or isinstance(product.quantity, bool):
            raise ValueError("Quantity must be an integer.")

        if not isinstance(product.minimum_stock, int) or isinstance(product.minimum_stock, bool):
            raise ValueError("Minimum stock must be an integer.")

        if product.quantity < 0:
            raise ValueError("Quantity cannot be negative.")

        if product.minimum_stock < 0:
            raise ValueError("Minimum stock cannot be negative.")

    def add_product(self, product):
        self.validate_product(product)

        connection = get_connection()

        try:
            connection.execute("""
                INSERT INTO products (
                    product_id,
                    name,
                    category,
                    purchase_price,
                    selling_price,
                    quantity,
                    minimum_stock
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product.product_id.strip(),
                product.name.strip(),
                product.category.strip(),
                str(product.purchase_price),
                str(product.selling_price),
                product.quantity,
                product.minimum_stock
            ))

            connection.commit()
            print("Product added successfully.")

        except sqlite3.IntegrityError as error:
            connection.rollback()
            print(f"Database error: {error}")

        except sqlite3.Error as error:
            connection.rollback()
            print(f"Unable to add product: {error}")

        finally:
            connection.close()

    def display_products(self):
        connection = get_connection()

        try:
            products = connection.execute("""
                SELECT * FROM products
                ORDER BY product_id
            """).fetchall()

            if not products:
                print("No products found.")
                return

            print("\n" + "-" * 105)
            print(
                f"{'ID':<10}"
                f"{'Name':<22}"
                f"{'Category':<18}"
                f"{'Purchase':>12}"
                f"{'Selling':>12}"
                f"{'Stock':>10}"
                f"{'Min Stock':>12}"
            )
            print("-" * 105)

            for product in products:
                print(
                    f"{product['product_id']:<10}"
                    f"{product['name']:<22}"
                    f"{product['category']:<18}"
                    f"{Decimal(str(product['purchase_price'] or 0)):>12.2f}"
                    f"{Decimal(str(product['selling_price'] or 0)):>12.2f}"
                    f"{product['quantity']:>10}"
                    f"{product['minimum_stock']:>12}"
                )

            print("-" * 105)

        except sqlite3.Error as error:
            print(f"Unable to display products: {error}")

        finally:
            connection.close()

    def search_product(self, keyword):
        connection = get_connection()

        try:
            product = connection.execute("""
                SELECT * FROM products
                WHERE product_id = ?
                   OR name LIKE ?
                ORDER BY name
            """, (
                keyword.strip(),
                f"%{keyword.strip()}%"
            )).fetchall()

            if not product:
                print("No matching products found.")
                return

            for item in product:
                print(dict(item))

        except sqlite3.Error as error:
            print(f"Search failed: {error}")

        finally:
            connection.close()

    def update_product(
        self,
        product_id,
        name,
        category,
        purchase_price,
        selling_price,
        minimum_stock
    ):
        connection = get_connection()

        try:
            existing = connection.execute("""
                SELECT quantity FROM products
                WHERE product_id = ?
            """, (product_id,)).fetchone()

            if existing is None:
                print("Product not found.")
                return

            product = Product(
                product_id=product_id,
                name=name,
                category=category,
                purchase_price=purchase_price,
                selling_price=selling_price,
                quantity=existing["quantity"],
                minimum_stock=minimum_stock
            )

            self.validate_product(product)

            connection.execute("""
                UPDATE products
                SET name = ?,
                    category = ?,
                    purchase_price = ?,
                    selling_price = ?,
                    minimum_stock = ?
                WHERE product_id = ?
            """, (
                name.strip(),
                category.strip(),
                str(purchase_price),
                str(selling_price),
                minimum_stock,
                product_id
            ))

            connection.commit()
            print("Product updated successfully.")

        except ValueError as error:
            connection.rollback()
            print(f"Invalid product information: {error}")

        except sqlite3.Error as error:
            connection.rollback()
            print(f"Unable to update product: {error}")

        finally:
            connection.close()

    def delete_product(self, product_id):
        connection = get_connection()

        try:
            existing = connection.execute("""
                SELECT product_id
                FROM products
                WHERE product_id = ?
            """, (product_id,)).fetchone()

            if existing is None:
                print("Product not found.")
                return

            connection.execute("""
                DELETE FROM products
                WHERE product_id = ?
            """, (product_id,))

            connection.commit()
            print("Product deleted successfully.")

        except sqlite3.IntegrityError:
            connection.rollback()
            print(
                "Cannot delete this product because it is "
                "referenced by existing purchase or sales records."
            )

        except sqlite3.Error as error:
            connection.rollback()
            print(f"Unable to delete product: {error}")

        finally:
            connection.close()

    def sort_products(self, sort_by="name", descending=False):
        allowed_columns = {
            "name": "name",
            "purchase_price": "purchase_price",
            "selling_price": "selling_price",
            "quantity": "quantity"
        }

        if sort_by not in allowed_columns:
            raise ValueError("Invalid sorting option.")

        order = "DESC" if descending else "ASC"
        column = allowed_columns[sort_by]

        connection = get_connection()

        try:
            products = connection.execute(
                f"""
                SELECT * FROM products
                ORDER BY {column} {order}, product_id ASC
                """
            ).fetchall()

            for product in products:
                print(dict(product))

            if not products:
                print("No products available to sort.")

        except sqlite3.Error as error:
            print(f"Unable to sort products: {error}")

        finally:
            connection.close()