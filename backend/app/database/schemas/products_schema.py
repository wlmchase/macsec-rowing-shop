from pydantic import BaseModel, UUID4


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: UUID4

    class Config:
        from_attributes = True