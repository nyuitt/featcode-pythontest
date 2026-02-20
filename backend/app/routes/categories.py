from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import category as crud_category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    existing = crud_category.get_category_by_name(db, name=category_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Categoria com nome '{category_in.name}' já existe."
        )
    return crud_category.create_category(db, category_in=category_in)

@router.get("/", response_model=list[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_category.get_categories(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: str, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria '{category_id}' não encontrada."
        )
    return db_category

@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: str, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria '{category_id}' não encontrada."
        )
    return crud_category.update_category(db, db_category=db_category, category_in=category_in)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    deleted = crud_category.delete_category(db, category_id=category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria '{category_id}' não encontrada."
        )
