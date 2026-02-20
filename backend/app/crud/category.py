from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
import uuid

def get_category(db: Session, category_id: str) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str) -> Category | None:
    return db.query(Category).filter(Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> list[Category]:
    return db.query(Category).offset(skip).limit(limit).all()

def create_category(db: Session, category_in: CategoryCreate) -> Category:
    db_category = Category(
        id=str(uuid.uuid4()),
        **category_in.model_dump()
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, db_category: Category, category_in: CategoryUpdate) -> Category:
    update_data = category_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: str) -> bool:
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return False
    db.delete(db_category)
    db.commit()
    return True
