import sqlite3
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from database import get_connection


class SalesManager:

    def create_sale(self, items, discount=Decimal("0.00"), tax_rate=Decimal("0.00")):
        if not isinstance(items, list) or not items:
            raise ValueError("A sale must contain at least one product.")

        try:
            discount = Decimal(str(discount))
            tax_rate = Decimal(str(tax_rate))
        except (InvalidOperation, ValueError):
            raise ValueError("Discount and tax rate must be valid numbers.")

        if not discount.is_finite() or not tax_rate.is_finite():
            raise ValueError("Discount and tax rate must be finite numbers.")

        if discount < 0 or tax_rate < 0:
            raise ValueError("Discount and tax rate cannot be negative.")

        if tax_rate > Decimal("100"):
            raise ValueError("Tax rate cannot exceed 100%.")

        discount = discount.quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        connection = get_connection()

        try:
            connection.execute("BEGIN IMMEDIATE")

            prepared_items = []
            subtotal = Decimal("0.00")

            for item in items:
                if not isinstance(item, dict):
                    raise ValueError("Each sale item must be a dictionary.")

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
                    SELECT
                        product_id,
                        name,
                        quantity,
                        selling_price,
                        purchase_price
                    FROM products
                    WHERE product_id = ?
                    """,
                    (product_id.strip(),)
                ).fetchone()

                if product is None:
                    raise ValueError(
                        f"Product {product_id} does not exist."
                    )

                if product["quantity"] < quantity:
                    raise ValueError(
                        f"Insufficient stock for {product['name']}. "
                        f"Available: {product['quantity']}, "
                        f"Requested: {quantity}"
                    )

                selling_price = Decimal(str(product["selling_price"]))
                purchase_price = Decimal(str(product["purchase_price"]))

                if (
                    not selling_price.is_finite()
                    or not purchase_price.is_finite()
                    or selling_price < 0
                    or purchase_price < 0
                ):
                    raise ValueError("Invalid product price.")

                line_subtotal = (
                    selling_price * quantity
                ).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP
                )

                subtotal += line_subtotal

                prepared_items.append({
                    "product_id": product["product_id"],
                    "name": product["name"],
                    "quantity": quantity,
                    "selling_price": selling_price,
                    "purchase_price": purchase_price,
                    "subtotal": line_subtotal
                })

            subtotal = subtotal.quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            if discount > subtotal:
                raise ValueError(
                    "Discount cannot exceed the sale subtotal."
                )

            taxable_amount = subtotal - discount

            tax = (
                taxable_amount * tax_rate / Decimal("100")
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )

            final_amount = taxable_amount + tax

            sale_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor = connection.execute(
                """
                INSERT INTO sales (
                    invoice_number,
                    sale_date,
                    subtotal,
                    discount,
                    tax,
                    final_amount
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    "PENDING",
                    sale_date,
                    str(subtotal),
                    str(discount),
                    str(tax),
                    str(final_amount)
                )
            )

            sale_id = cursor.lastrowid
            invoice_number = f"INV{sale_id + 1000}"

            connection.execute(
                """
                UPDATE sales
                SET invoice_number = ?
                WHERE sale_id = ?
                """,
                (invoice_number, sale_id)
            )

            for item in prepared_items:
                connection.execute(
                    """
                    INSERT INTO sale_items (
                        sale_id,
                        product_id,
                        quantity,
                        selling_price,
                        purchase_price,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sale_id,
                        item["product_id"],
                        item["quantity"],
                        str(item["selling_price"]),
                        str(item["purchase_price"]),
                        str(item["subtotal"])
                    )
                )

                cursor = connection.execute(
                    """
                    UPDATE products
                    SET quantity = quantity - ?
                    WHERE product_id = ?
                      AND quantity >= ?
                    """,
                    (
                        item["quantity"],
                        item["product_id"],
                        item["quantity"]
                    )
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        f"Unable to update stock for {item['name']}."
                    )

            connection.commit()

            print("\n========== SALE INVOICE ==========")
            print(f"Invoice Number: {invoice_number}")
            print(f"Date: {sale_date}")

            for item in prepared_items:
                print(
                    f"{item['name']} | "
                    f"Quantity: {item['quantity']} | "
                    f"Price: Rs. {item['selling_price']:.2f} | "
                    f"Subtotal: Rs. {item['subtotal']:.2f}"
                )

            print(f"Subtotal: Rs. {subtotal:.2f}")
            print(f"Discount: Rs. {discount:.2f}")
            print(f"Tax: Rs. {tax:.2f}")
            print(f"Final Amount: Rs. {final_amount:.2f}")
            print("Sale completed successfully!")

            return sale_id

        except (ValueError, InvalidOperation) as error:
            connection.rollback()
            print(f"Sale failed: {error}")
            return None

        except sqlite3.Error as error:
            connection.rollback()
            print(f"Database error: {error}")
            return None

        finally:
            connection.close()

    def display_sales(self):
        connection = get_connection()

        try:
            sales = connection.execute(
                """
                SELECT *
                FROM sales
                ORDER BY sale_id DESC
                """
            ).fetchall()

            if not sales:
                print("No sales found.")
                return

            print("\n========== SALES HISTORY ==========")

            for sale in sales:
                print(
                    f"Invoice: {sale['invoice_number']} | "
                    f"Date: {sale['sale_date']} | "
                    f"Amount: Rs. "
                    f"{Decimal(str(sale['final_amount'])):.2f}"
                )

        except sqlite3.Error as error:
            print(f"Unable to display sales: {error}")

        finally:
            connection.close()

    def display_invoice(self, invoice_number):
        connection = get_connection()

        try:
            sale = connection.execute(
                """
                SELECT *
                FROM sales
                WHERE invoice_number = ?
                """,
                (invoice_number,)
            ).fetchone()

            if sale is None:
                print("Invoice not found.")
                return

            items = connection.execute(
                """
                SELECT
                    p.name,
                    si.product_id,
                    si.quantity,
                    si.selling_price,
                    si.subtotal
                FROM sale_items si
                JOIN products p
                    ON si.product_id = p.product_id
                WHERE si.sale_id = ?
                """,
                (sale["sale_id"],)
            ).fetchall()

            print("\n========== INVOICE DETAILS ==========")
            print(f"Invoice Number: {sale['invoice_number']}")
            print(f"Date: {sale['sale_date']}")

            for item in items:
                print(
                    f"{item['name']} | "
                    f"Product ID: {item['product_id']} | "
                    f"Quantity: {item['quantity']} | "
                    f"Price: Rs. "
                    f"{Decimal(str(item['selling_price'])):.2f} | "
                    f"Subtotal: Rs. "
                    f"{Decimal(str(item['subtotal'])):.2f}"
                )

            print(
                f"Subtotal: Rs. "
                f"{Decimal(str(sale['subtotal'])):.2f}"
            )
            print(
                f"Discount: Rs. "
                f"{Decimal(str(sale['discount'])):.2f}"
            )
            print(
                f"Tax: Rs. "
                f"{Decimal(str(sale['tax'])):.2f}"
            )
            print(
                f"Final Amount: Rs. "
                f"{Decimal(str(sale['final_amount'])):.2f}"
            )

        except sqlite3.Error as error:
            print(f"Unable to retrieve invoice: {error}")

        finally:
            connection.close()