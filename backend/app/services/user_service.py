from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models.models import User
from app.database.repository.user_repo import get_user_by_id, get_all_users as repo_get_all_users
from app.database.repository.user_repo import update_user as repo_update_user
from app.database.repository.user_repo import delete_user as repo_delete_user
from app.database.repository.user_repo import get_user_by_email
from app.database.schemas.users_schema import UserUpdate
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

async def get_all_users(db: AsyncSession) -> list[User]:
    """Get all users from the database"""
    try:
        users = await repo_get_all_users(db)
        return users  # Return empty list if no users found
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users from database"
        )

async def get_user(db: AsyncSession, user_id: str) -> User:
    """Get a specific user by ID"""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

async def update_user(db: AsyncSession, user_id: str, user_update: UserUpdate) -> User:
    """Update a user's information"""
    try:
        updated_user = await repo_update_user(db, user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

async def delete_user(db: AsyncSession, user_id: str) -> None:
    """Delete a user"""
    deleted_user = await repo_delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
