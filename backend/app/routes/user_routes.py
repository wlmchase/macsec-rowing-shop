from app.config.dependency import get_current_admin_user, get_current_user
from app.database.models.models import User
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from app.config.database import get_db
from app.database.schemas.users_schema import UserResponse, UserUpdate, UserCreate
from app.services import user_service
from typing import List, Annotated
from fastapi.responses import JSONResponse
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.validation import validate_email, validate_password
#from fastapi_limiter import FastAPILimiter
#from fastapi_limiter.depends import RateLimiter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

### Current User Routes ###
@router.get(
    "/me",
    response_model=UserResponse
)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's profile
    
    Returns:
    - The current user's profile information
    """
    try:
        return current_user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )

### Admin Routes ###
#@limiter.limit("5/minute")
@router.get(
    "/all-users",
    response_model=List[UserResponse]
)
async def all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """
    Get all users (admin only)
    """
    try:
        return await user_service.get_all_users(db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

### Regular Routes ###

# Update user info
#@limiter.limit("5/minute")
@router.put(
    "/update-user/{user_id}",
    response_model=UserResponse
)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update user profile (owner or admin only)
    
    Parameters:
    - user_id: The ID of the user to update
    - user_update: The user data to update
    """
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    # Validate email if being updated
    if user_update.email is not None:
        is_valid_email, email_error = validate_email(user_update.email)
        if not is_valid_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=email_error
            )

    # Validate password if being updated
    if user_update.password is not None:
        is_valid_password, password_error = validate_password(user_update.password)
        if not is_valid_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=password_error
            )

    return await user_service.update_user(db, user_id, user_update)

# Delete user
#@limiter.limit("5/minute")
@router.delete(
    "/delete-user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete user profile (owner or admin only)
    
    Parameters:
    - user_id: The ID of the user to delete
    """
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )
    await user_service.delete_user(db, user_id)
    return None

### PROFILE ####
#@limiter.limit("5/minute")
@router.get(
    "/profile/{user_id}",
    response_model=UserResponse
)
async def get_profile(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get user profile (owner or admin only)
    
    Parameters:
    - user_id: The ID of the user to retrieve
    """
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this profile"
        )
    return await user_service.get_user(db, user_id)
