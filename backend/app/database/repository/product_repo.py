from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.models import Product
from ..schemas.products_schema import ProductCreate, ProductUpdate

### PRODUCTS ###

# Create a new product
async def create_product(db: AsyncSession, product: ProductCreate) -> Product :
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# Get all products
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Product] :
    stmt = select(Product).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().unique().all()

# Get product by id
async def get_product(db: AsyncSession, product_id: str) -> Product | None :
    stmt = select(Product).filter(Product.id == product_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# Update product by id
async def update_product(db: AsyncSession, product_id: str, product: ProductUpdate) -> Product | None :
    stmt = select(Product).filter(Product.id == product_id)
    result = await db.execute(stmt)
    db_product = result.scalar_one_or_none()
    
    if db_product:
        for key, value in product.model_dump().items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product)
    return db_product

# Delete product by id
async def delete_product(db: AsyncSession, product_id: str) -> bool :
    stmt = select(Product).filter(Product.id == product_id)
    result = await db.execute(stmt)
    db_product = result.scalar_one_or_none()
    
    if db_product:
        await db.delete(db_product)
        await db.commit()
        return True
    return False