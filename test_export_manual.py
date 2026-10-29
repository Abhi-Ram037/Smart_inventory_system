from report_exporter import ReportExporter


def test_csv_export():
    exporter = ReportExporter()

    print("\n--- EXPORT INVENTORY REPORT ---")
    exporter.export_inventory()

    print("\n--- EXPORT SALES REPORT ---")
    exporter.export_sales()


if __name__ == "__main__":
    test_csv_export()