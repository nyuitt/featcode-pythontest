from sqlalchemy.orm import Session
from sqlalchemy import func
from decimal import Decimal

from app.models.product import Product
from app.models.category import Category
from app.schemas.dashboard import DashboardResponse, CategorySummary, ProductLowStock

LOW_STOCK_THRESHOLD = 10


def get_dashboard_data(db: Session) -> DashboardResponse:
    total_products: int = db.query(func.count(Product.id)).scalar() or 0

    total_stock_value: Decimal = db.query(
        func.coalesce(func.sum(Product.price * Product.stock), 0)
    ).scalar()

    low_stock_products = (
        db.query(Product)
        .filter(Product.stock < LOW_STOCK_THRESHOLD)
        .all()
    )

    per_category_rows = (
        db.query(
            Product.category_id,
            Category.name.label("category_name"),
            func.count(Product.id).label("product_count"),
        )
        .outerjoin(Category, Product.category_id == Category.id)
        .group_by(Product.category_id, Category.name)
        .all()
    )

    return DashboardResponse(
        total_products=total_products,
        total_stock_value=Decimal(str(total_stock_value)),
        low_stock_count=len(low_stock_products),
        low_stock_products=[ProductLowStock.model_validate(p) for p in low_stock_products],
        products_by_category=[
            CategorySummary(
                category_id=row.category_id,
                category_name=row.category_name or "Sem categoria",
                product_count=row.product_count,
            )
            for row in per_category_rows
        ],
    )
