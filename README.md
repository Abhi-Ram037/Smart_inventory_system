# Smart Inventory and Sales Management System

## Project Overview

The Smart Inventory and Sales Management System is a Python-based application designed to manage product inventory, suppliers, purchases, sales, and business reports. It uses SQLite as its database to store and manage information efficiently.

The system helps businesses maintain accurate stock quantities, track sales transactions, manage suppliers, generate invoices, and analyze business performance through reports.

## Features

### 1. Product Management
- Add new products.
- Display all available products.
- Search products by ID or name.
- Update product details.
- Delete products.
- Sort products by name, price, or stock quantity.
- Prevent duplicate product IDs.
- Validate product prices and quantities.

### 2. Supplier Management
- Add suppliers.
- Display supplier information.
- Search suppliers.
- Update supplier details.
- View supplier purchase history.

### 3. Purchase Management
- Record purchases from suppliers.
- Support multiple products in one purchase.
- Automatically increase stock quantities.
- Calculate purchase totals.
- Display purchase history and purchase details.

### 4. Sales Management
- Generate unique invoice numbers.
- Sell multiple products in a single transaction.
- Automatically decrease stock quantities.
- Apply discounts and taxes.
- Calculate invoice totals.
- Prevent sales when stock is insufficient.
- Display sales history and invoices.

### 5. Inventory Management
- View low-stock products.
- Identify out-of-stock products.
- Calculate inventory value.
- Display the top-selling products.
- Track stock movement history.

### 6. Business Analytics
- Daily sales reports.
- Weekly sales reports.
- Monthly sales reports.
- Revenue and purchase expense reports.
- Gross profit analysis by product.
- Best-selling and least-selling products.
- Category-wise sales analysis.
- Sales reports for a specified date range.

### 7. Report Export
- Export inventory reports to CSV.
- Export sales reports to CSV.
- Open exported reports using spreadsheet applications.

## Technologies Used

- Python
- SQLite3
- SQL
- Object-Oriented Programming
- Dataclasses
- Decimal for monetary calculations
- CSV file handling
- Exception handling
- Unit testing

The project uses Python's standard library and does not require third-party packages for its core functionality.

## Project Structure

```text
smart_inventory_system/
│
├── main.py
├── database.py
├── models.py
├── product_manager.py
├── supplier_manager.py
├── purchase_manager.py
├── sales_manager.py
├── inventory_manager.py
├── analytics_manager.py
├── report_exporter.py
│
├── test_system.py
├── test_business.py
│
├── database/
│   └── inventory.db
│
├── reports/
│   ├── inventory_report.csv
│   └── sales_report.csv
│
├── venv/
├── .gitignore
└── README.md
```

Additional manual test files may also be present in the project directory.

## Installation and Setup

### Step 1: Install Python

Install Python 3.10 or a compatible newer version.

Verify the installation:

```bash
python --version
```

### Step 2: Open the Project Directory

```powershell
cd D:\python\smart_inventory_system
```

### Step 3: Create a Virtual Environment

```powershell
python -m venv venv
```

### Step 4: Activate the Virtual Environment

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If the virtual environment is already activated, you can skip this step.

### Step 5: Initialize the Database

```powershell
python database.py
```

This creates the required database tables and indexes if they do not already exist.

### Step 6: Run the Application

```powershell
python main.py
```

The application displays a menu through which you can manage products, suppliers, purchases, sales, inventory reports, analytics, and CSV exports.

## Running the Tests

Run the business logic tests:

```powershell
python -m unittest test_business.py -v
```

Run the basic database tests:

```powershell
python -m unittest test_system.py -v
```

Run tests discovered automatically:

```powershell
python -m unittest discover -v
```

The business logic tests use a temporary database to test important operations without modifying the main inventory database.

## Database Design

The application uses six main tables:

| Table | Purpose |
|---|---|
| `products` | Stores product information, prices, and stock quantities. |
| `suppliers` | Stores supplier contact information. |
| `purchases` | Stores purchase transaction records. |
| `purchase_items` | Stores individual products included in purchases. |
| `sales` | Stores sales transactions and invoice totals. |
| `sale_items` | Stores individual products included in sales. |

Foreign keys connect related records. Database transactions help maintain consistency when purchases and sales update multiple records.

## Reports Generated

The application can export reports such as:

- `inventory_report.csv`
- `sales_report.csv`

These files are stored in the `reports` directory.

## Learning Outcomes

This project demonstrates practical experience with:

- Python programming.
- Object-oriented programming.
- SQLite database integration.
- SQL queries and relational database design.
- CRUD operations.
- Transaction management.
- Input validation and exception handling.
- Inventory and sales calculations.
- CSV report generation.
- Unit testing.
- Modular application development.

## Conclusion

The Smart Inventory and Sales Management System demonstrates how Python and SQLite can be combined to develop a practical business application. It integrates inventory control, supplier management, purchasing, sales processing, invoicing, reporting, and business analytics into a single menu-driven system.