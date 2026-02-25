from app.database.repository import user_repo
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.database.schemas.users_schema import UserCreate, UserResponse
from app.database.schemas.auth_schema import ChangePass
from app.config.database import get_db
from app.config.dependency import get_current_user
from app.database.models.models import User
from app.database.schemas.auth_schema import Token, TokenData, TokenResponse, LoginRequest
from app.services import auth_service 
from app.core.security import oauth2_scheme
from app.core.validation import validate_email, validate_password
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

# ROUTER -> SERVICE -> REPOSITORY -> DB

### REFRESH TOKEN ####
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token."""
    new_token = await auth_service.refresh_token(db, refresh_token)
    if not new_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    return new_token


### LOGIN ####
@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
    ):
    """Login user and return access token."""
    token = await auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return token


### LOGOUT ####
@router.post("/logout")
async def logout(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """Logout endpoint that blacklists the current token."""
    await auth_service.blacklist_token(db, token)
    return {"message": "Successfully logged out"}

### REGISTER ####
@router.post("/register", response_model=UserResponse)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    # Validate email
    is_valid_email, email_error = validate_email(user.email)
    if not is_valid_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=email_error
        )

    # Validate password
    is_valid_password, password_error = validate_password(user.password)
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=password_error
        )

    # Check if user already exists
    db_user = await auth_service.register_user(db, user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return db_user

### CHANGE PASS ####
@router.post("/change-password")
async def change_password(
    change_pass: ChangePass,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    """Change user password"""
    # Validate new password
    is_valid_password, password_error = validate_password(change_pass.new)
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=password_error
        )

    try:
        response = await auth_service.change_password(db, token, current_user, change_pass)
        return response
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )