from decimal import Decimal

from models import Product
from product_manager import ProductManager


manager = ProductManager()


def test_product_management():
    product = Product(
        product_id="P101",
        name="Chocolate Cake",
        category="Bakery",
        purchase_price=Decimal("300.00"),
        selling_price=Decimal("450.00"),
        quantity=20,
        minimum_stock=5
    )

    manager.add_product(product)

    print("\n--- ALL PRODUCTS ---")
    manager.display_products()

    print("\n--- SEARCH PRODUCT ---")
    manager.search_product("P101")

    print("\n--- SORT BY SELLING PRICE ---")
    manager.sort_products("selling_price")

    print("\n--- UPDATE PRODUCT ---")
    manager.update_product(
        product_id="P101",
        name="Chocolate Cake",
        category="Bakery",
        purchase_price=Decimal("320.00"),
        selling_price=Decimal("480.00"),
        minimum_stock=5
    )

    print("\n--- PRODUCTS AFTER UPDATE ---")
    manager.display_products()


if __name__ == "__main__":
    test_product_management()