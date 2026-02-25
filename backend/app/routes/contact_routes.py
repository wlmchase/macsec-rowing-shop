from app.config.dependency import get_current_admin_user
from app.database.models.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from app.config.database import get_db
from app.services import contact_service
from app.database.schemas.contact_schema import ContactBase, ContactResponse
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/contact",
    tags=["contact"],
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

### CONTACT ####

@router.post("/", response_model=ContactResponse)
async def create_contact(
    contact: ContactBase,
    db: AsyncSession = Depends(get_db)
):
    """Create a new contact message"""
    return await contact_service.create_contact(db, contact)

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all contact messages (admin only)"""
    return await contact_service.get_contacts(db)

@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get a specific contact message by ID (admin only)"""
    contact = await contact_service.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact message not found"
        )
    return contact