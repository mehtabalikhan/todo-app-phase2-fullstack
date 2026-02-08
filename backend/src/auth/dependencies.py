from fastapi import Depends, HTTPException, status, Request
from typing import Dict, Any
from src.auth.jwt_handler import verify_token, get_user_id_from_token_payload


async def get_current_user(request: Request) -> Dict[str, Any]:
    """
    Dependency to get the current user from the request state.
    This assumes that the AuthMiddleware has already verified the token
    and added user information to the request state.
    """
    if not hasattr(request.state, 'user_id') or request.state.user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "user_id": request.state.user_id,
        "token_payload": getattr(request.state, 'token_payload', {})
    }


async def get_user_id_from_token(authorization: str = None) -> str:
    """
    Alternative dependency to extract user ID directly from authorization header.
    This can be used when middleware is not in place.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.split(" ")[1]
    payload = verify_token(token)
    user_id = get_user_id_from_token_payload(payload)
    return user_id


def require_active_user(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Wrapper dependency to require an active user.
    This can be used to enforce that a valid user is present.
    """
    # Here we could add additional checks for user status (active, suspended, etc.)
    # For now, just ensure the user exists
    if not current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user