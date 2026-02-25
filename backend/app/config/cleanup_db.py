from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

async def cleanup_database(session: AsyncSession) -> None:
    """
    Cleans up all tables in the database by truncating them.
    This should be called when shutting down the application.
    """
    # Get all table names
    result = await session.execute(text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'"))
    tables = [row[0] for row in result]
    
    # Disable foreign key constraints temporarily
    await session.execute(text("SET CONSTRAINTS ALL DEFERRED"))
    
    # Truncate all tables
    for table in tables:
        await session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
    
    await session.commit() 