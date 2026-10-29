import sqlite3
from database import get_connection


class Supplier:
    def __init__(self, supplier_id, name, phone, address):
        self.supplier_id = supplier_id
        self.name = name
        self.phone = phone
        self.address = address


class SupplierManager:

    def validate_supplier(self, supplier):
        if not supplier.supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")

        if not supplier.name.strip():
            raise ValueError("Supplier name cannot be empty.")

        if not supplier.phone.strip():
            raise ValueError("Phone number cannot be empty.")

        if not supplier.address.strip():
            raise ValueError("Address cannot be empty.")

    def add_supplier(self, supplier):
        try:
            self.validate_supplier(supplier)

            connection = get_connection()

            try:
                connection.execute("""
                    INSERT INTO suppliers (
                        supplier_id,
                        name,
                        phone,
                        address
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    supplier.supplier_id.strip(),
                    supplier.name.strip(),
                    supplier.phone.strip(),
                    supplier.address.strip()
                ))

                connection.commit()
                print("Supplier added successfully.")

            finally:
                connection.close()

        except ValueError as error:
            print(f"Invalid supplier details: {error}")

        except sqlite3.IntegrityError:
            print("Supplier ID already exists.")

        except sqlite3.Error as error:
            print(f"Database error: {error}")

    def display_suppliers(self):
        connection = get_connection()

        try:
            suppliers = connection.execute("""
                SELECT *
                FROM suppliers
                ORDER BY supplier_id
            """).fetchall()

            if not suppliers:
                print("No suppliers found.")
                return

            print("\n" + "-" * 80)
            print(
                f"{'Supplier ID':<15}"
                f"{'Name':<25}"
                f"{'Phone':<18}"
                f"{'Address':<22}"
            )
            print("-" * 80)

            for supplier in suppliers:
                print(
                    f"{supplier['supplier_id']:<15}"
                    f"{supplier['name']:<25}"
                    f"{supplier['phone']:<18}"
                    f"{supplier['address']:<22}"
                )

            print("-" * 80)

        except sqlite3.Error as error:
            print(f"Unable to display suppliers: {error}")

        finally:
            connection.close()

    def search_supplier(self, keyword):
        connection = get_connection()

        try:
            suppliers = connection.execute("""
                SELECT *
                FROM suppliers
                WHERE supplier_id = ?
                   OR name LIKE ?
                ORDER BY name
            """, (
                keyword.strip(),
                f"%{keyword.strip()}%"
            )).fetchall()

            if not suppliers:
                print("No matching suppliers found.")
                return

            for supplier in suppliers:
                print(dict(supplier))

        except sqlite3.Error as error:
            print(f"Search failed: {error}")

        finally:
            connection.close()

    def update_supplier(self, supplier_id, name, phone, address):
        supplier = Supplier(
            supplier_id,
            name,
            phone,
            address
        )

        try:
            self.validate_supplier(supplier)

            connection = get_connection()

            try:
                cursor = connection.execute("""
                    UPDATE suppliers
                    SET name = ?,
                        phone = ?,
                        address = ?
                    WHERE supplier_id = ?
                """, (
                    name.strip(),
                    phone.strip(),
                    address.strip(),
                    supplier_id.strip()
                ))

                if cursor.rowcount == 0:
                    print("Supplier not found.")
                    return

                connection.commit()
                print("Supplier updated successfully.")

            finally:
                connection.close()

        except ValueError as error:
            print(f"Invalid supplier details: {error}")

        except sqlite3.Error as error:
            print(f"Unable to update supplier: {error}")

    def supplier_purchase_history(self, supplier_id):
        connection = get_connection()

        try:
            supplier = connection.execute("""
                SELECT name
                FROM suppliers
                WHERE supplier_id = ?
            """, (supplier_id,)).fetchone()

            if supplier is None:
                print("Supplier not found.")
                return

            purchases = connection.execute("""
                SELECT
                    purchase_id,
                    purchase_date,
                    total_amount
                FROM purchases
                WHERE supplier_id = ?
                ORDER BY purchase_date DESC, purchase_id DESC
            """, (supplier_id,)).fetchall()

            print(f"\nPurchase History: {supplier['name']}")

            if not purchases:
                print("No purchases found for this supplier.")
                return

            total_spending = 0

            for purchase in purchases:
                amount = float(purchase["total_amount"])
                total_spending += amount

                print(
                    f"Purchase ID: {purchase['purchase_id']} | "
                    f"Date: {purchase['purchase_date']} | "
                    f"Amount: Rs. {amount:.2f}"
                )

            print(f"Total Purchase Amount: Rs. {total_spending:.2f}")

        except sqlite3.Error as error:
            print(f"Unable to retrieve purchase history: {error}")

        finally:
            connection.close()