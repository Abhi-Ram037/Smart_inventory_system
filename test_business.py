import unittest
import sqlite3
import tempfile
from pathlib import Path
from decimal import Decimal
from unittest.mock import patch

import database
from database import get_connection, initialize_database
from models import Product
from product_manager import ProductManager
from purchase_manager import PurchaseManager
from sales_manager import SalesManager


class BusinessLogicTests(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        database_directory = Path(self.temp_directory.name) / "database"

        self.directory_patch = patch.object(
            database, "DATABASE_DIR", database_directory
        )
        self.path_patch = patch.object(
            database,
            "DATABASE_PATH",
            database_directory / "test_inventory.db"
        )

        self.directory_patch.start()
        self.path_patch.start()

        initialize_database()

        self.product_manager = ProductManager()
        self.purchase_manager = PurchaseManager()
        self.sales_manager = SalesManager()

        self.add_test_product()

        connection = get_connection()

        try:
            connection.execute("""
                INSERT INTO suppliers
                (supplier_id, name, phone, address)
                VALUES (?, ?, ?, ?)
            """, ("SUP1", "Test Supplier", "9876543210", "Kadapa"))

            connection.commit()
        finally:
            connection.close()

    def tearDown(self):
        self.path_patch.stop()
        self.directory_patch.stop()
        self.temp_directory.cleanup()

    def add_test_product(self):
        product = Product(
            product_id="P1",
            name="Test Product",
            category="General",
            purchase_price=Decimal("10.00"),
            selling_price=Decimal("20.00"),
            quantity=10,
            minimum_stock=2
        )

        self.product_manager.add_product(product)

    def get_stock(self):
        connection = get_connection()

        try:
            product = connection.execute("""
                SELECT quantity
                FROM products
                WHERE product_id = 'P1'
            """).fetchone()

            return product["quantity"]
        finally:
            connection.close()

    def test_duplicate_product_id_is_rejected(self):
        product = Product(
            product_id="P1",
            name="Duplicate Product",
            category="General",
            purchase_price=Decimal("10.00"),
            selling_price=Decimal("20.00"),
            quantity=5,
            minimum_stock=2
        )

        self.product_manager.add_product(product)

        connection = get_connection()

        try:
            result = connection.execute("""
                SELECT COUNT(*) AS total
                FROM products
                WHERE product_id = 'P1'
            """).fetchone()

            self.assertEqual(result["total"], 1)
        finally:
            connection.close()

    def test_negative_purchase_price_fails_validation(self):
        product = Product(
            product_id="P2",
            name="Invalid Product",
            category="General",
            purchase_price=Decimal("-10.00"),
            selling_price=Decimal("20.00"),
            quantity=5,
            minimum_stock=2
        )

        with self.assertRaises(ValueError):
            self.product_manager.validate_product(product)

    def test_purchase_increases_stock(self):
        purchase_id = self.purchase_manager.create_purchase(
            "SUP1",
            [{"product_id": "P1", "quantity": 5}]
        )

        self.assertIsNotNone(purchase_id)
        self.assertEqual(self.get_stock(), 15)

    def test_sale_decreases_stock(self):
        sale_id = self.sales_manager.create_sale(
            [{"product_id": "P1", "quantity": 3}],
            discount=Decimal("0.00"),
            tax_rate=Decimal("0.00")
        )

        self.assertIsNotNone(sale_id)
        self.assertEqual(self.get_stock(), 7)

    def test_sale_with_insufficient_stock_is_rejected(self):
        sale_id = self.sales_manager.create_sale(
            [{"product_id": "P1", "quantity": 20}],
            discount=Decimal("0.00"),
            tax_rate=Decimal("0.00")
        )

        self.assertIsNone(sale_id)
        self.assertEqual(self.get_stock(), 10)

    def test_invoice_total_is_calculated_correctly(self):
        sale_id = self.sales_manager.create_sale(
            [{"product_id": "P1", "quantity": 2}],
            discount=Decimal("5.00"),
            tax_rate=Decimal("0.00")
        )

        self.assertIsNotNone(sale_id)

        connection = get_connection()

        try:
            sale = connection.execute("""
                SELECT invoice_number, subtotal, discount, final_amount
                FROM sales
                WHERE sale_id = ?
            """, (sale_id,)).fetchone()

            self.assertTrue(sale["invoice_number"].startswith("INV"))
            self.assertEqual(Decimal(str(sale["subtotal"])), Decimal("40"))
            self.assertEqual(Decimal(str(sale["discount"])), Decimal("5"))
            self.assertEqual(Decimal(str(sale["final_amount"])), Decimal("35"))

        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)