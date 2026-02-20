from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.limiter import limiter
from app.crud import product as crud_product
from app.schemas.product import ProductCreate, ProductUpdate, ProductStockUpdate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/low-stock", response_model=list[ProductResponse])
@limiter.limit("60/minute")
def list_low_stock(request: Request, db: Session = Depends(get_db)):
    return crud_product.get_low_stock_products(db)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
def create_product(request: Request, product_in: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product_in=product_in)


@router.get("/", response_model=list[ProductResponse])
@limiter.limit("100/minute")
def list_products(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    category_id: str | None = None,
    db: Session = Depends(get_db),
):
    return crud_product.get_products(db, skip=skip, limit=limit, search=search, category_id=category_id)


@router.get("/{product_id}", response_model=ProductResponse)
@limiter.limit("100/minute")
def get_product(request: Request, product_id: str, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto '{product_id}' não encontrado.")
    return db_product


@router.patch("/{product_id}", response_model=ProductResponse)
@limiter.limit("30/minute")
def update_product(request: Request, product_id: str, product_in: ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto '{product_id}' não encontrado.")
    return crud_product.update_product(db, db_product=db_product, product_in=product_in)


@router.patch("/{product_id}/stock", response_model=ProductResponse)
@limiter.limit("30/minute")
def update_stock(request: Request, product_id: str, stock_in: ProductStockUpdate, db: Session = Depends(get_db)):
    db_product = crud_product.get_product(db, product_id=product_id)
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto '{product_id}' não encontrado.")
    return crud_product.update_stock(db, db_product=db_product, stock_in=stock_in)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
def delete_product(request: Request, product_id: str, db: Session = Depends(get_db)):
    deleted = crud_product.delete_product(db, product_id=product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Produto '{product_id}' não encontrado.")
