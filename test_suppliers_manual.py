from supplier_manager import Supplier, SupplierManager


manager = SupplierManager()


def test_supplier_management():
    supplier = Supplier(
        supplier_id="SUP101",
        name="ABC Distributors",
        phone="9876543210",
        address="Kadapa"
    )

    manager.add_supplier(supplier)

    print("\n--- ALL SUPPLIERS ---")
    manager.display_suppliers()

    print("\n--- SEARCH SUPPLIER ---")
    manager.search_supplier("SUP101")

    print("\n--- UPDATE SUPPLIER ---")
    manager.update_supplier(
        supplier_id="SUP101",
        name="ABC Wholesale Distributors",
        phone="9876543210",
        address="Tirupati"
    )

    print("\n--- SUPPLIERS AFTER UPDATE ---")
    manager.display_suppliers()

    print("\n--- SUPPLIER PURCHASE HISTORY ---")
    manager.supplier_purchase_history("SUP101")


if __name__ == "__main__":
    test_supplier_management()