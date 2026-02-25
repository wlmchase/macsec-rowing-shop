from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.models import User, Role
from app.core.security_utils import get_password_hash
from app.database.repository.product_repo import create_product
from app.database.schemas.products_schema import ProductCreate

async def init_db(db: AsyncSession) -> None:
    # Create admin user if it doesn't exist
    stmt = select(User).filter(User.email == "admin@example.com")
    result = await db.execute(stmt)
    admin = result.scalar_one_or_none()
    
    if not admin:
        admin = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role=Role.ADMIN,
            is_active=True
        )
        db.add(admin)
        await db.commit()

    # Create dummy user
    stmt = select(User).filter(User.email == "user@example.com")
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:    
        user = User(
            email="user@example.com",
            hashed_password=get_password_hash("user123"),
            role=Role.USER,
            is_active=True
        )
        db.add(user)
        await db.commit()


    # Create initial products
    # Add sample products if none exist
    products = [
        ProductCreate(
            name="Double Scull",
            description="Boat for two rowers",
            price=12000.00,
            stock=3
        ),
        ProductCreate(
            name="Carbon Fiber Oars",
            description="Lightweight racing oars",
            price=400.00,
            stock=20
        ),
        ProductCreate(
            name="Rowing Hat",
            description="Protection against sun and rain",
            price=25.00,
            stock=100
        )
    ]
    
    for product in products:
        await create_product(db, product) 