from analytics_manager import AnalyticsManager

analytics = AnalyticsManager()


def test_analytics():
    print("\n1. DAILY SALES")
    analytics.display_daily_sales()

    print("\n2. WEEKLY SALES")
    analytics.display_weekly_sales()

    print("\n3. MONTHLY SALES")
    analytics.display_monthly_sales()

    print("\n4. REVENUE AND PURCHASE EXPENSES")
    analytics.display_revenue_and_expenses()

    print("\n5. GROSS PROFIT BY PRODUCT")
    analytics.display_gross_profit_by_product()

    print("\n6. BEST AND LEAST-SELLING PRODUCTS")
    analytics.display_best_and_least_selling_products()

    print("\n7. CATEGORY-WISE SALES")
    analytics.display_category_wise_sales()

    print("\n8. DATE-RANGE SALES")
    analytics.display_sales_by_date_range(
        "2026-10-27",
        "2026-10-27"
    )


if __name__ == "__main__":
    test_analytics()