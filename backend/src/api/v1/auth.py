from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_session
from src.schemas.user import UserCreate, Token
from src.models.user import User
from src.services.user_service import UserService
from src.auth.jwt_handler import create_access_token
from src.auth.dependencies import get_current_user
from src.auth.exceptions import InvalidCredentialsException
from src.utils.logging import log_security_event

router = APIRouter()


@router.post("/register", response_model=Token)
async def register_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Register a new user.

    Creates a new user account with the provided credentials.
    """
    user_service = UserService(db)

    try:
        # Check if user already exists
        existing_user = await user_service.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Create the new user
        user = await user_service.create_user(user_create)

        # Create access token for the new user
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"user_id": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        # Log successful registration
        log_security_event("USER_REGISTRATION", f"New user registered: {user.email}", str(user.id))

        return Token(access_token=access_token, token_type="bearer")

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        log_security_event("FAILED_USER_REGISTRATION", str(e), "unknown")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while registering the user"
        )


@router.post("/login", response_model=Token)
async def login_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    """
    Authenticate user and return access token.

    Validates user credentials and returns an access token if valid.
    """
    user_service = UserService(db)

    try:
        # Verify user credentials
        user = await user_service.verify_password(user_create.email, user_create.password)

        if not user:
            raise InvalidCredentialsException(detail="Incorrect email or password")

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"user_id": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )

        # Log successful login
        log_security_event("USER_LOGIN", f"User logged in: {user.email}", str(user.id))

        return Token(access_token=access_token, token_type="bearer")

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        log_security_event("FAILED_USER_LOGIN", str(e), "unknown")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while logging in"
        )


@router.post("/logout")
async def logout_user(
    current_user: dict = Depends(get_current_user)
):
    """
    Logout the current user.

    Performs server-side logout operations.
    """
    user_id = current_user["user_id"]

    try:
        # In a real implementation, we might add the token to a blacklist
        # For now, we just log the logout event

        log_security_event("USER_LOGOUT", f"User logged out: {current_user.get('email', user_id)}", user_id)

        return {"message": "Successfully logged out"}

    except Exception as e:
        log_security_event("FAILED_USER_LOGOUT", str(e), user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while logging out"
        )


# Include this for testing purposes
@router.get("/me")
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """
    Get current user information.

    Returns information about the currently authenticated user.
    """
    user_id = current_user["user_id"]

    return {
        "id": user_id,
        "email": current_user.get("email"),
        "message": "Current user information retrieved successfully"
    }