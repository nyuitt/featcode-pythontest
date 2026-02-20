from pydantic import BaseModel, Field
from decimal import Decimal


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    description: str | None = Field(None, max_length=1000)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(..., ge=0)
    category_id: str | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=255)
    description: str | None = Field(None, max_length=1000)
    price: Decimal | None = Field(None, gt=0, decimal_places=2)
    stock: int | None = Field(None, ge=0)
    category_id: str | None = None


class ProductStockUpdate(BaseModel):
    stock: int = Field(..., ge=0)


class ProductResponse(ProductBase):
    id: str

    model_config = {"from_attributes": True}
