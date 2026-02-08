from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, status
from src.config.settings import get_settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token with the given data"""
    settings = get_settings()

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.better_auth_jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify a JWT token and return the payload if valid"""
    settings = get_settings()

    try:
        payload = jwt.decode(token, settings.better_auth_jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_token_without_validation(token: str) -> dict:
    """Decode a JWT token without validating the signature (for inspection purposes only)"""
    from src.config.settings import get_settings
    settings = get_settings()

    try:
        # Decode without verification - only use for inspection!
        payload = jwt.decode(token, options={"verify_signature": False}, algorithms=[settings.jwt_algorithm])
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not decode token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_id_from_token_payload(payload: dict) -> str:
    """Extract user ID from token payload"""
    user_id = payload.get("user_id") or payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials - no user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return str(user_id)