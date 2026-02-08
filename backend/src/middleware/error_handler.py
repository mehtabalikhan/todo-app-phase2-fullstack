from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from typing import Callable
import traceback
import logging
from datetime import datetime
import uuid

from src.auth.exceptions import AuthException, InvalidCredentialsException, ExpiredTokenException, \
    InsufficientPermissionsException, ResourceNotFoundException, ValidationErrorException, \
    InternalServerErrorException, create_error_response


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Comprehensive error handling middleware for the application"""

    def __init__(self, app):
        super().__init__(app)
        self.logger = logging.getLogger(__name__)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except AuthException as e:
            # Handle custom authentication exceptions
            self.logger.warning(f"Auth error: {e.detail} (Request ID: {getattr(e, 'request_id', 'unknown')})")

            error_response = {
                "detail": e.detail,
                "error_code": e.error_code,
                "timestamp": e.timestamp,
                "request_id": e.request_id
            }
            return JSONResponse(status_code=e.status_code, content=error_response)

        except HTTPException as e:
            # Handle standard HTTP exceptions
            request_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()

            self.logger.info(f"HTTP error {e.status_code}: {e.detail} (Request ID: {request_id})")

            # Map some error codes to our standard format
            error_code_map = {
                400: "REQ_001",  # Malformed request
                401: "AUTH_001",  # Invalid credentials
                403: "AUTH_003",  # Insufficient permissions
                404: "DATA_001",  # Resource not found
                422: "DATA_002",  # Validation error
                500: "SYS_001"   # Internal server error
            }

            error_code = error_code_map.get(e.status_code, f"REQ_{e.status_code}")

            error_response = {
                "detail": e.detail,
                "error_code": error_code,
                "timestamp": timestamp,
                "request_id": request_id
            }
            return JSONResponse(status_code=e.status_code, content=error_response)

        except Exception as e:
            # Handle unexpected errors
            request_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()

            error_msg = str(e)
            self.logger.error(f"Unexpected error: {error_msg}\nTraceback: {traceback.format_exc()}",
                            extra={"request_id": request_id})

            error_response = {
                "detail": "An internal server error occurred",
                "error_code": "SYS_001",
                "timestamp": timestamp,
                "request_id": request_id
            }
            return JSONResponse(status_code=500, content=error_response)


def add_error_handling_middleware(app):
    """Helper function to add error handling middleware to the application"""
    app.add_middleware(ErrorHandlerMiddleware)
    return app