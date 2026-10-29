from decimal import Decimal, InvalidOperation

from database import initialize_database, get_connection
from models import Product
from product_manager import ProductManager
from supplier_manager import SupplierManager, Supplier
from purchase_manager import PurchaseManager
from sales_manager import SalesManager
from inventory_manager import Inventory
from analytics_manager import AnalyticsManager
from report_exporter import ReportExporter


product_manager = ProductManager()
supplier_manager = SupplierManager()
purchase_manager = PurchaseManager()
sales_manager = SalesManager()
inventory = Inventory()
analytics = AnalyticsManager()
exporter = ReportExporter()


def get_integer(prompt, minimum=None):
    value = int(input(prompt))

    if minimum is not None and value < minimum:
        raise ValueError(f"Value must be at least {minimum}.")

    return value


def get_decimal(prompt):
    value = Decimal(input(prompt))

    if not value.is_finite():
        raise ValueError("Enter a valid number.")

    return value


def display_menu():
    print("\n" + "=" * 55)
    print("   SMART INVENTORY AND SALES MANAGEMENT SYSTEM")
    print("=" * 55)

    print("\n--- PRODUCT MANAGEMENT ---")
    print("1. Add Product")
    print("2. Display Products")
    print("3. Search Product")
    print("4. Update Product")
    print("5. Delete Product")
    print("6. Sort Products")

    print("\n--- SUPPLIER MANAGEMENT ---")
    print("7. Add Supplier")
    print("8. Display Suppliers")
    print("9. Update Supplier")
    print("10. Search Supplier")

    print("\n--- PURCHASE MANAGEMENT ---")
    print("11. Create Purchase")
    print("12. Display Purchase History")
    print("13. Display Purchase Details")

    print("\n--- SALES MANAGEMENT ---")
    print("14. Create Sale")
    print("15. Display Sales History")
    print("16. Display Invoice")

    print("\n--- INVENTORY REPORTS ---")
    print("17. Low Stock Report")
    print("18. Out-of-Stock Report")
    print("19. Inventory Valuation")
    print("20. Top 5 Best-Selling Products")
    print("21. Stock Movement History")

    print("\n--- SALES ANALYTICS ---")
    print("22. Daily Sales Report")
    print("23. Weekly Sales Report")
    print("24. Monthly Sales Report")
    print("25. Revenue and Purchase Expenses")
    print("26. Gross Profit by Product")
    print("27. Best and Least-Selling Products")
    print("28. Category-Wise Sales")
    print("29. Sales by Date Range")

    print("\n--- EXPORT REPORTS ---")
    print("30. Export Inventory to CSV")
    print("31. Export Sales to CSV")

    print("\n0. Exit")
    print("=" * 55)


def add_product():
    product = Product(
        product_id=input("Enter Product ID: ").strip(),
        name=input("Enter Product Name: ").strip(),
        category=input("Enter Category: ").strip(),
        purchase_price=get_decimal("Enter Purchase Price: "),
        selling_price=get_decimal("Enter Selling Price: "),
        quantity=get_integer("Enter Initial Quantity: ", 0),
        minimum_stock=get_integer("Enter Minimum Stock: ", 0)
    )

    product_manager.add_product(product)


def search_product():
    keyword = input("Enter Product ID or Name: ").strip()
    product_manager.search_product(keyword)


def update_product():
    product_id = input("Enter Product ID to update: ").strip()

    name = input("Enter New Product Name: ").strip()
    category = input("Enter New Category: ").strip()
    purchase_price = get_decimal("Enter New Purchase Price: ")
    selling_price = get_decimal("Enter New Selling Price: ")
    minimum_stock = get_integer("Enter New Minimum Stock: ", 0)

    product_manager.update_product(
        product_id,
        name,
        category,
        purchase_price,
        selling_price,
        minimum_stock
    )


def delete_product():
    product_id = input("Enter Product ID to delete: ").strip()

    confirmation = input(
        f"Are you sure you want to delete {product_id}? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        product_manager.delete_product(product_id)
    else:
        print("Delete operation cancelled.")


def sort_products():
    print("\nSort By:")
    print("1. Product Name")
    print("2. Purchase Price")
    print("3. Selling Price")
    print("4. Quantity")

    choice = input("Enter choice: ").strip()

    sort_options = {
        "1": "name",
        "2": "purchase_price",
        "3": "selling_price",
        "4": "quantity"
    }

    if choice not in sort_options:
        print("Invalid sorting option.")
        return

    order = input("Descending order? (yes/no): ").strip().lower()

    product_manager.sort_products(
        sort_by=sort_options[choice],
        descending=(order == "yes")
    )


def add_supplier():
    supplier = Supplier(
        supplier_id=input("Enter Supplier ID: ").strip(),
        name=input("Enter Supplier Name: ").strip(),
        phone=input("Enter Phone Number: ").strip(),
        address=input("Enter Address: ").strip()
    )

    supplier_manager.add_supplier(supplier)


def update_supplier():
    supplier_id = input("Enter Supplier ID: ").strip()
    name = input("Enter New Supplier Name: ").strip()
    phone = input("Enter New Phone Number: ").strip()
    address = input("Enter New Address: ").strip()

    supplier_manager.update_supplier(
        supplier_id,
        name,
        phone,
        address
    )


def search_supplier():
    keyword = input("Enter Supplier ID or Name: ").strip()
    supplier_manager.search_supplier(keyword)


def create_purchase():
    supplier_id = input("Enter Supplier ID: ").strip()
    items = []

    while True:
        product_id = input("Enter Product ID: ").strip()
        quantity = get_integer("Enter Purchase Quantity: ", 1)

        items.append({
            "product_id": product_id,
            "quantity": quantity
        })

        more = input("Add another product? (yes/no): ").strip().lower()

        if more != "yes":
            break

    purchase_manager.create_purchase(supplier_id, items)


def display_purchase_details():
    purchase_id = get_integer("Enter Purchase ID: ", 1)
    purchase_manager.display_purchase_details(purchase_id)


def create_sale():
    items = []

    while True:
        product_id = input("Enter Product ID: ").strip()
        quantity = get_integer("Enter Sale Quantity: ", 1)

        items.append({
            "product_id": product_id,
            "quantity": quantity
        })

        more = input("Add another product? (yes/no): ").strip().lower()

        if more != "yes":
            break

    discount = get_decimal("Enter Discount Amount: Rs. ")
    tax_rate = get_decimal("Enter Tax Rate Percentage: ")

    sales_manager.create_sale(
        items=items,
        discount=discount,
        tax_rate=tax_rate
    )


def display_invoice():
    invoice_number = input("Enter Invoice Number: ").strip()
    sales_manager.display_invoice(invoice_number)


def sales_by_date_range():
    start_date = input("Enter Start Date (YYYY-MM-DD): ").strip()
    end_date = input("Enter End Date (YYYY-MM-DD): ").strip()

    analytics.display_sales_by_date_range(start_date, end_date)


def run_application():
    initialize_database()

    actions = {
        "1": add_product,
        "2": product_manager.display_products,
        "3": search_product,
        "4": update_product,
        "5": delete_product,
        "6": sort_products,
        "7": add_supplier,
        "8": supplier_manager.display_suppliers,
        "9": update_supplier,
        "10": search_supplier,
        "11": create_purchase,
        "12": purchase_manager.display_purchases,
        "13": display_purchase_details,
        "14": create_sale,
        "15": sales_manager.display_sales,
        "16": display_invoice,
        "17": inventory.display_low_stock,
        "18": inventory.display_out_of_stock,
        "19": inventory.display_inventory_value,
        "20": inventory.display_top_selling_products,
        "21": inventory.display_stock_movement_history,
        "22": analytics.display_daily_sales,
        "23": analytics.display_weekly_sales,
        "24": analytics.display_monthly_sales,
        "25": analytics.display_revenue_and_expenses,
        "26": analytics.display_gross_profit_by_product,
        "27": analytics.display_best_and_least_selling_products,
        "28": analytics.display_category_wise_sales,
        "29": sales_by_date_range,
        "30": exporter.export_inventory,
        "31": exporter.export_sales
    }

    print("\nDatabase is ready.")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("\nThank you.")
            break

        action = actions.get(choice)

        if action is None:
            print("Invalid choice. Please select an option from the menu.")
            continue

        try:
            action()
        except (ValueError, InvalidOperation) as error:
            print(f"Invalid input: {error}")
        except sqlite3.Error as error:
            print(f"Database error: {error}")
        except Exception as error:
            print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    import sqlite3

    run_application()