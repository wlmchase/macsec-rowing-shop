from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repository.user_repo import get_user_by_email, create_user
from app.database.repository.token_repo import add_to_blacklist, cleanup_expired_tokens
from app.core.security_utils import verify_password, get_password_hash
from app.core import security
from datetime import datetime, timezone
import jwt
from jwt import PyJWTError as JWTError
from fastapi import HTTPException, status
from app.config import settings
from app.database.models.models import User
from app.database.schemas.users_schema import UserCreate
from app.database.schemas.auth_schema import TokenResponse, ChangePass
import logging

settings = settings.get_settings()
logger = logging.getLogger(__name__)


def create_access_token(data: dict) -> str:
    return security.create_access_token(data)


async def refresh_token(db: AsyncSession, token: str):
    try:
        # Verify the current token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims"
            )
            
        # Check if token is blacklisted
        if await security.is_token_blacklisted(db, token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been invalidated"
            )
            
        # Verify user still exists and is active
        user = await get_user_by_email(db, email)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
            
        # Create new token
        new_token = create_access_token({"sub": email})
        
        # Optionally blacklist the old token
        old_token_exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await add_to_blacklist(db, token, old_token_exp)
        
        return {
            "access_token": new_token,
            "token_type": "bearer"
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

async def authenticate_user(db: AsyncSession, email: str, password: str) -> TokenResponse:
    """Authenticate a user by email and password."""
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    # get an access token
    access_token = create_access_token({"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

async def blacklist_token(db: AsyncSession, token: str) -> None:
    """Add a token to the blacklist."""
    try:
        # Try to decode the token, but don't check expiration
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options={"verify_exp": False})
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        await add_to_blacklist(db, token, expires_at)
        await cleanup_expired_tokens(db)
    except JWTError as e:
        logger.error(f"Error blacklisting token: {str(e)}")
        # Even if token is invalid, we can still blacklist it
        await add_to_blacklist(db, token, datetime.now(timezone.utc))
        await cleanup_expired_tokens(db)

async def register_user(db: AsyncSession, user: UserCreate) -> User:
    """Register a new user."""
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        db_user = await create_user(db, user)
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register user: {str(e)}"
        )

async def change_password(db: AsyncSession, token: str, current_user: User, change_pass_data: ChangePass) -> dict:
    """Change user password."""
    try:
        # Get fresh user data from database
        user = await get_user_by_email(db, current_user.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Verify current password
        if not verify_password(change_pass_data.current, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        new_hashed_password = get_password_hash(change_pass_data.new)
        
        # Update user's password
        user.hashed_password = new_hashed_password
        await db.commit()
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {str(e)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )
