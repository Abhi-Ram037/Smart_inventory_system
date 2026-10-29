import csv
from pathlib import Path
from database import get_connection


BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"


class ReportExporter:

    def __init__(self):
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    def export_inventory(self):
        connection = get_connection()

        try:
            products = connection.execute("""
                SELECT
                    product_id,
                    name,
                    category,
                    purchase_price,
                    selling_price,
                    quantity,
                    minimum_stock,
                    quantity * purchase_price AS inventory_value
                FROM products
                ORDER BY name
            """).fetchall()

            file_path = REPORTS_DIR / "inventory_report.csv"

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Product ID",
                    "Product Name",
                    "Category",
                    "Purchase Price",
                    "Selling Price",
                    "Quantity",
                    "Minimum Stock",
                    "Inventory Value"
                ])

                for product in products:
                    writer.writerow([
                        product["product_id"],
                        product["name"],
                        product["category"],
                        product["purchase_price"],
                        product["selling_price"],
                        product["quantity"],
                        product["minimum_stock"],
                        product["inventory_value"]
                    ])

            print("\nInventory report exported successfully.")
            print(f"File location: {file_path}")
            return file_path

        except (OSError, csv.Error) as error:
            print(f"File export error: {error}")
            return None

        except Exception as error:
            print(f"Error exporting inventory: {error}")
            return None

        finally:
            connection.close()

    def export_sales(self):
        connection = get_connection()

        try:
            sales = connection.execute("""
                SELECT
                    invoice_number,
                    sale_date,
                    subtotal,
                    discount,
                    tax,
                    final_amount
                FROM sales
                ORDER BY sale_date DESC
            """).fetchall()

            file_path = REPORTS_DIR / "sales_report.csv"

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:
                writer = csv.writer(file)

                writer.writerow([
                    "Invoice Number",
                    "Sale Date",
                    "Subtotal",
                    "Discount",
                    "Tax",
                    "Final Amount"
                ])

                for sale in sales:
                    writer.writerow([
                        sale["invoice_number"],
                        sale["sale_date"],
                        sale["subtotal"],
                        sale["discount"],
                        sale["tax"],
                        sale["final_amount"]
                    ])

            print("\nSales report exported successfully.")
            print(f"File location: {file_path}")
            return file_path

        except (OSError, csv.Error) as error:
            print(f"File export error: {error}")
            return None

        except Exception as error:
            print(f"Error exporting sales: {error}")
            return None

        finally:
            connection.close()