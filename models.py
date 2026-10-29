from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Product:
    product_id: str
    name: str
    category: str
    purchase_price: Decimal
    selling_price: Decimal
    quantity: int
    minimum_stock: int = 5