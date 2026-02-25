from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import Product
from app.database.repository import product_repo
from app.database.schemas.products_schema import ProductCreate, ProductUpdate

async def get_all_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Product]:
    """Retrieve all products with pagination."""
    return await product_repo.get_products(db, skip, limit)

async def get_product_by_id(db: AsyncSession, product_id: str) -> Product | None:
    """Retrieve a product by its ID."""
    return await product_repo.get_product(db, product_id)

async def create_product(db: AsyncSession, product: ProductCreate) -> Product:
    """Create a new product."""
    return await product_repo.create_product(db, product)

async def update_product(db: AsyncSession, product_id: str, product: ProductUpdate) -> Product | None:
    """Update a product by its ID."""
    return await product_repo.update_product(db, product_id, product)

async def delete_product(db: AsyncSession, product_id: str) -> bool:
    """Delete a product by its ID."""
    return await product_repo.delete_product(db, product_id)