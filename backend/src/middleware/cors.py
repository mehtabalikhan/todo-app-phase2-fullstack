from fastapi.middleware.cors import CORSMiddleware
from typing import List
from src.config.settings import get_settings


def add_cors_middleware(app):
    """
    Add CORS middleware to the FastAPI application
    This allows the frontend to make requests to the backend
    """
    settings = get_settings()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Requested-With", "X-Client-Type"],
        # Expose headers that frontend may need to access
        expose_headers=["Access-Control-Allow-Origin", "Access-Control-Allow-Credentials"],
        # Set max age to reduce preflight requests
        max_age=86400,  # 24 hours
    )

    return app