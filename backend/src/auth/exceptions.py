from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
import uuid


class AuthException(HTTPException):
    """Base authentication exception with standardized error format"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str,
        headers: Optional[dict] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code
        self.timestamp = datetime.utcnow().isoformat()
        self.request_id = str(uuid.uuid4())


class InvalidCredentialsException(AuthException):
    """Exception raised when credentials are invalid"""

    def __init__(self, detail: str = "Invalid authentication credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH_001"
        )


class ExpiredTokenException(AuthException):
    """Exception raised when token has expired"""

    def __init__(self, detail: str = "Token has expired"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTH_002"
        )


class InsufficientPermissionsException(AuthException):
    """Exception raised when user lacks sufficient permissions"""

    def __init__(self, detail: str = "Insufficient permissions to access this resource"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTH_003"
        )


class ResourceNotFoundException(AuthException):
    """Exception raised when requested resource is not found"""

    def __init__(self, detail: str = "Requested resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="DATA_001"
        )


class ValidationErrorException(AuthException):
    """Exception raised when data validation fails"""

    def __init__(self, detail: str = "Data validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="DATA_002"
        )


class InternalServerErrorException(AuthException):
    """Exception raised when an internal server error occurs"""

    def __init__(self, detail: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="SYS_001"
        )


def create_error_response(error_code: str, detail: str, status_code: int):
    """Helper function to create standardized error responses"""
    return {
        "detail": detail,
        "error_code": error_code,
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": str(uuid.uuid4())
    }


def handle_auth_exception(request, exc: AuthException):
    """Exception handler for authentication exceptions"""
    return create_error_response(
        error_code=exc.error_code,
        detail=exc.detail,
        status_code=exc.status_code
    )