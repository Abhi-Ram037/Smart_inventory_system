from inventory_manager import Inventory

inventory = Inventory()


def test_inventory():
    print("\n1. LOW STOCK REPORT")
    inventory.display_low_stock()

    print("\n2. OUT OF STOCK REPORT")
    inventory.display_out_of_stock()

    print("\n3. INVENTORY VALUATION")
    inventory.display_inventory_value()

    print("\n4. TOP SELLING PRODUCTS")
    inventory.display_top_selling_products()

    print("\n5. STOCK MOVEMENT HISTORY")
    inventory.display_stock_movement_history()


if __name__ == "__main__":
    test_inventory()