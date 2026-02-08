from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from typing import Optional
import re
from src.auth.jwt_handler import verify_token, get_user_id_from_token_payload


class JWTBearer(HTTPBearer):
    """Custom JWT Bearer authentication scheme"""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Wrong authentication scheme."
                )
            token = credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No authorization header provided"
            )

        return verify_token(token)


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware to verify JWT tokens on protected routes"""

    # Routes that don't require authentication
    excluded_routes = [
        "/",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/login",
        "/api/v1/register",
        "/api/v1/logout",
        "/api/v1/refresh",
        # Also include any potential auth routes that don't require auth
        "/api/auth/login",
        "/api/auth/register",
        "/api/auth/logout",
        "/api/auth/refresh",
    ]

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Check if the route should be excluded from auth
        if (request.url.path in self.excluded_routes or
            self._is_openapi_route(request.url.path) or
            self._is_auth_route(request.url.path)):
            response = await call_next(request)
            return response

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid format"
            )

        token = auth_header.split(" ")[1]

        try:
            # Verify the token
            payload = verify_token(token)
            user_id = get_user_id_from_token_payload(payload)

            # Add user info to request state for use in route handlers
            request.state.user_id = user_id
            request.state.token_payload = payload

        except HTTPException:
            # Re-raise HTTP exceptions (like invalid token)
            raise
        except Exception:
            # Handle any other errors in token verification
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        response = await call_next(request)
        return response

    def _is_openapi_route(self, path: str) -> bool:
        """Check if the route is an OpenAPI documentation route"""
        openapi_patterns = [
            r"/docs(/.*)?$",
            r"/redoc(/.*)?$",
            r"/openapi\.json$",
            r"/swagger\.json$",
            r"/swagger\.ui(/.*)?$"
        ]

        for pattern in openapi_patterns:
            if re.match(pattern, path):
                return True
        return False

    def _is_auth_route(self, path: str) -> bool:
        """Check if the route is an authentication route that doesn't require auth"""
        auth_patterns = [
            r"/api/v1/login$",
            r"/api/v1/register$",
            r"/api/v1/logout$",
            r"/api/v1/refresh$",
            r"/api/auth/login$",
            r"/api/auth/register$",
            r"/api/auth/logout$",
            r"/api/auth/refresh$",
        ]

        for pattern in auth_patterns:
            if re.match(pattern, path):
                return True
        return False