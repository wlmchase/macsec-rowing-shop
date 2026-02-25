from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.models import User
from app.database.schemas.users_schema import UserCreate, UserUpdate
from app.core.security_utils import get_password_hash

### USER ###

async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    """Get a user by their ID"""
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Get a user by their email"""
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_all_users(db: AsyncSession) -> list[User]:
    """Get all users"""
    stmt = select(User)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: str, user_update: UserUpdate) -> User | None:
    """Update a user's information"""
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        return None
        
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        if field == "password":
            value = get_password_hash(value)
            field = "hashed_password"
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def delete_user(db: AsyncSession, user_id: str) -> User | None:
    """Delete a user"""
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    db_user = result.scalar_one_or_none()
    
    if not db_user:
        return None
    
    await db.delete(db_user)
    await db.commit()
    return db_user