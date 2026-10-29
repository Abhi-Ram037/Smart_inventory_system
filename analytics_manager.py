import sqlite3
from decimal import Decimal
from database import get_connection


class AnalyticsManager:

    def display_daily_sales(self):
        connection = get_connection()

        try:
            records = connection.execute("""
                SELECT
                    DATE(sale_date) AS sales_day,
                    COUNT(*) AS total_orders,
                    SUM(final_amount) AS revenue
                FROM sales
                GROUP BY DATE(sale_date)
                ORDER BY sales_day DESC
            """).fetchall()

            print("\n========== DAILY SALES REPORT ==========")

            if not records:
                print("No sales records found.")
                return

            for record in records:
                print(
                    f"Date: {record['sales_day']} | "
                    f"Orders: {record['total_orders']} | "
                    f"Revenue: Rs. {Decimal(str(record['revenue'])):.2f}"
                )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()

    def display_weekly_sales(self):
        connection = get_connection()

        try:
            records = connection.execute("""
                SELECT
                    STRFTIME('%Y-W%W', sale_date) AS sales_week,
                    COUNT(*) AS total_orders,
                    SUM(final_amount) AS revenue
                FROM sales
                GROUP BY STRFTIME('%Y-W%W', sale_date)
                ORDER BY sales_week DESC
            """).fetchall()

            print("\n========== WEEKLY SALES REPORT ==========")

            if not records:
                print("No sales records found.")
                return

            for record in records:
                print(
                    f"Week: {record['sales_week']} | "
                    f"Orders: {record['total_orders']} | "
                    f"Revenue: Rs. {Decimal(str(record['revenue'])):.2f}"
                )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()

    def display_monthly_sales(self):
        connection = get_connection()

        try:
            records = connection.execute("""
                SELECT
                    STRFTIME('%Y-%m', sale_date) AS sales_month,
                    COUNT(*) AS total_orders,
                    SUM(final_amount) AS revenue
                FROM sales
                GROUP BY STRFTIME('%Y-%m', sale_date)
                ORDER BY sales_month DESC
            """).fetchall()

            print("\n========== MONTHLY SALES REPORT ==========")

            if not records:
                print("No sales records found.")
                return

            for record in records:
                print(
                    f"Month: {record['sales_month']} | "
                    f"Orders: {record['total_orders']} | "
                    f"Revenue: Rs. {Decimal(str(record['revenue'])):.2f}"
                )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()

    def display_revenue_and_expenses(self):
        connection = get_connection()

        try:
            sales = connection.execute("""
                SELECT COALESCE(SUM(final_amount), 0) AS revenue
                FROM sales
            """).fetchone()

            purchases = connection.execute("""
                SELECT COALESCE(SUM(total_amount), 0) AS expenses
                FROM purchases
            """).fetchone()

            revenue = Decimal(str(sales["revenue"]))
            expenses = Decimal(str(purchases["expenses"]))

            print("\n========== REVENUE AND PURCHASE EXPENSES ==========")
            print(f"Total Sales Revenue: Rs. {revenue:.2f}")
            print(f"Total Purchase Expenses: Rs. {expenses:.2f}")
            print(f"Difference: Rs. {revenue - expenses:.2f}")
            print(
                "Note: This difference is not net profit. "
                "It does not account for unsold stock or other expenses."
            )

        except (sqlite3.Error, ArithmeticError, ValueError) as error:
            print(f"Error generating report: {error}")

        finally:
            connection.close()

    def display_gross_profit_by_product(self):
        connection = get_connection()

        try:
            records = connection.execute("""
                SELECT
                    p.product_id,
                    p.name,
                    SUM(si.quantity) AS quantity_sold,
                    SUM(si.selling_price * si.quantity) AS sales_value,
                    SUM(si.purchase_price * si.quantity) AS cost_value,
                    SUM(
                        (si.selling_price - si.purchase_price)
                        * si.quantity
                    ) AS gross_profit
                FROM sale_items si
                INNER JOIN products p
                    ON si.product_id = p.product_id
                GROUP BY p.product_id, p.name
                ORDER BY gross_profit DESC
            """).fetchall()

            print("\n========== GROSS PROFIT BY PRODUCT ==========")

            if not records:
                print("No sales records found.")
                return

            for record in records:
                profit = Decimal(str(record["gross_profit"]))

                print(
                    f"Product: {record['name']} | "
                    f"ID: {record['product_id']} | "
                    f"Quantity Sold: {record['quantity_sold']} | "
                    f"Sales Value: Rs. {Decimal(str(record['sales_value'])):.2f} | "
                    f"Cost: Rs. {Decimal(str(record['cost_value'])):.2f} | "
                    f"Gross Profit: Rs. {profit:.2f}"
                )

            print(
                "Note: The calculation uses item prices before invoice-level "
                "discounts and taxes."
            )

        except (sqlite3.Error, ArithmeticError, ValueError) as error:
            print(f"Error generating report: {error}")

        finally:
            connection.close()

    def display_best_and_least_selling_products(self):
        connection = get_connection()

        try:
            records = connection.execute("""
                SELECT
                    p.product_id,
                    p.name,
                    COALESCE(SUM(si.quantity), 0) AS quantity_sold
                FROM products p
                LEFT JOIN sale_items si
                    ON p.product_id = si.product_id
                GROUP BY p.product_id, p.name
                ORDER BY quantity_sold DESC, p.name ASC
            """).fetchall()

            print("\n========== BEST AND LEAST-SELLING PRODUCTS ==========")

            if not records:
                print("No products found.")
                return

            best_selling = records[0]
            least_selling = records[-1]

            print(
                f"Best-Selling Product: {best_selling['name']} | "
                f"Quantity Sold: {best_selling['quantity_sold']}"
            )

            print(
                f"Least-Selling Product: {least_selling['name']} | "
                f"Quantity Sold: {least_selling['quantity_sold']}"
            )

        except sqlite3.Error as error:
            print(f"Database error: {error}")

        finally:
            connection.close()

    def display_category_wise_sales(self):
        connection = get_connection()

        try:
            records = connection.execute("""
                SELECT
                    p.category,
                    SUM(si.quantity) AS quantity_sold,
                    SUM(si.selling_price * si.quantity) AS sales_value
                FROM sale_items si
                INNER JOIN products p
                    ON si.product_id = p.product_id
                GROUP BY p.category
                ORDER BY sales_value DESC
            """).fetchall()

            print("\n========== CATEGORY-WISE SALES ==========")

            if not records:
                print("No sales records found.")
                return

            for record in records:
                print(
                    f"Category: {record['category']} | "
                    f"Quantity Sold: {record['quantity_sold']} | "
                    f"Sales Value: Rs. {Decimal(str(record['sales_value'])):.2f}"
                )

        except (sqlite3.Error, ArithmeticError, ValueError) as error:
            print(f"Error generating report: {error}")

        finally:
            connection.close()

    def display_sales_by_date_range(self, start_date, end_date):
        connection = get_connection()

        try:
            if not start_date or not end_date:
                print("Both start date and end date are required.")
                return

            start = sqlite3.Date if False else start_date
            end = end_date

            from datetime import datetime

            start = datetime.strptime(start, "%Y-%m-%d").date()
            end = datetime.strptime(end, "%Y-%m-%d").date()

            if start > end:
                print("Start date cannot be after end date.")
                return

            records = connection.execute("""
                SELECT
                    invoice_number,
                    sale_date,
                    subtotal,
                    discount,
                    tax,
                    final_amount
                FROM sales
                WHERE DATE(sale_date) BETWEEN ? AND ?
                ORDER BY sale_date
            """, (start.isoformat(), end.isoformat())).fetchall()

            print("\n========== DATE-RANGE SALES REPORT ==========")
            print(f"From: {start} To: {end}")

            if not records:
                print("No sales found for this date range.")
                return

            total_revenue = Decimal("0.00")

            for record in records:
                amount = Decimal(str(record["final_amount"]))
                total_revenue += amount

                print(
                    f"Invoice: {record['invoice_number']} | "
                    f"Date: {record['sale_date']} | "
                    f"Amount: Rs. {amount:.2f}"
                )

            print(f"Total Orders: {len(records)}")
            print(f"Total Revenue: Rs. {total_revenue:.2f}")

        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format, for example 2026-10-27.")

        except (sqlite3.Error, ArithmeticError) as error:
            print(f"Error generating report: {error}")

        finally:
            connection.close()