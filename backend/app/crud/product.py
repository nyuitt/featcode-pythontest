import structlog
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductStockUpdate
import uuid

log = structlog.get_logger("crud.product")


def get_product(db: Session, product_id: str) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    category_id: str | None = None,
) -> list[Product]:
    query = db.query(Product)
    if search:
        query = query.filter(func.lower(Product.name).contains(search.lower()))
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()


def get_low_stock_products(db: Session, threshold: int = 10) -> list[Product]:
    return db.query(Product).filter(Product.stock < threshold).all()


def create_product(db: Session, product_in: ProductCreate) -> Product:
    db_product = Product(
        id=str(uuid.uuid4()),
        **product_in.model_dump(),
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    log.info("product.created", product_id=db_product.id, name=db_product.name, price=str(db_product.price))
    return db_product


def update_product(db: Session, db_product: Product, product_in: ProductUpdate) -> Product:
    update_data = product_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    log.info("product.updated", product_id=db_product.id, fields=list(update_data.keys()))
    return db_product


def update_stock(db: Session, db_product: Product, stock_in: ProductStockUpdate) -> Product:
    old_stock = db_product.stock
    db_product.stock = stock_in.stock
    db.commit()
    db.refresh(db_product)
    log.info("product.stock_updated", product_id=db_product.id, old_stock=old_stock, new_stock=db_product.stock)
    return db_product


def delete_product(db: Session, product_id: str) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        log.warning("product.not_found", product_id=product_id)
        return False
    db.delete(db_product)
    db.commit()
    log.info("product.deleted", product_id=product_id)
    return True
