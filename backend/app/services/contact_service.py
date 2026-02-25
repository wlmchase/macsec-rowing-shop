from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repository import contact_repo
from app.database.schemas.contact_schema import ContactBase
import uuid

async def get_contact_by_id(db: AsyncSession, contact_id: str):
    return await contact_repo.get_contact_by_id(db, uuid.UUID(contact_id))

async def create_contact(db: AsyncSession, contact: ContactBase):
    return await contact_repo.create_contact(db, contact)

async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await contact_repo.get_contacts(db, skip, limit)