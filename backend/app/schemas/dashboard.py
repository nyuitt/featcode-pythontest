from pydantic import BaseModel
from decimal import Decimal


class CategorySummary(BaseModel):
    category_id: str | None
    category_name: str | None
    product_count: int


class ProductLowStock(BaseModel):
    id: str
    name: str
    stock: int
    category_id: str | None

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    total_products: int
    total_categories: int
    total_stock_value: Decimal
    low_stock_count: int
    low_stock_products: list[ProductLowStock]
    products_by_category: list[CategorySummary]
