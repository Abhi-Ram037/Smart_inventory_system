import unittest

from database import initialize_database, get_connection


class DatabaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        initialize_database()

    def test_required_tables_exist(self):
        connection = get_connection()

        try:
            rows = connection.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
            """).fetchall()

            table_names = {row["name"] for row in rows}

            required_tables = {
                "products",
                "suppliers",
                "purchases",
                "purchase_items",
                "sales",
                "sale_items"
            }

            self.assertTrue(required_tables.issubset(table_names))

        finally:
            connection.close()

    def test_products_table_has_records(self):
        connection = get_connection()

        try:
            result = connection.execute("""
                SELECT COUNT(*) AS total
                FROM products
            """).fetchone()

            self.assertGreater(result["total"], 0)

        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)