from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.models import ContactForm
from ..schemas.contact_schema import ContactBase
import uuid


### CONTACT ###
async def create_contact(db: AsyncSession, contact: ContactBase) -> ContactForm:
    new_contact = ContactForm(email=contact.email, message=contact.message)
    db.add(new_contact)
    await db.commit()
    await db.refresh(new_contact)
    return new_contact

async def get_contact_by_id(db: AsyncSession, contact_id: uuid.UUID) -> ContactForm | None:
    stmt = select(ContactForm).filter(ContactForm.id == contact_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_contacts(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[ContactForm]:
    stmt = select(ContactForm).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()