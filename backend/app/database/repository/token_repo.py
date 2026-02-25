from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database.models.models import TokenBlacklist
from datetime import datetime, timezone

async def is_token_blacklisted(db: AsyncSession, token: str) -> bool:
    """Check if a token is blacklisted"""
    stmt = select(TokenBlacklist).filter(TokenBlacklist.token == token)
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None

async def add_to_blacklist(db: AsyncSession, token: str, expires_at: datetime) -> TokenBlacklist:
    """Add a token to the blacklist"""
    # Convert timezone-aware datetime to naive datetime
    if expires_at.tzinfo is not None:
        expires_at = expires_at.astimezone(timezone.utc).replace(tzinfo=None)
    
    blacklisted_at = datetime.now(timezone.utc).astimezone(timezone.utc).replace(tzinfo=None)
    
    db_blacklist = TokenBlacklist(
        token=token,
        expires_at=expires_at,
        blacklisted_at=blacklisted_at
    )
    db.add(db_blacklist)
    await db.commit()
    await db.refresh(db_blacklist)
    return db_blacklist

async def cleanup_expired_tokens(db: AsyncSession) -> None:
    """Remove expired tokens from the blacklist"""
    current_time = datetime.now(timezone.utc).astimezone(timezone.utc).replace(tzinfo=None)
    stmt = select(TokenBlacklist).filter(TokenBlacklist.expires_at <= current_time)
    result = await db.execute(stmt)
    for token in result.scalars():
        await db.delete(token)
    await db.commit() 