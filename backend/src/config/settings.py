from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Database Configuration
    database_url: str = Field(default="", env="DATABASE_URL")

    # JWT Configuration
    better_auth_jwt_secret: str = Field(default="dev-secret-key-change-in-production", env="BETTER_AUTH_JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # CORS Configuration
    allowed_origins: List[str] = Field(default=["http://localhost:3000"], env="ALLOWED_ORIGINS")

    # Frontend URL
    frontend_url: str = Field(default="http://localhost:3001", env="FRONTEND_URL")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Environment
    environment: str = Field(default="development", env="ENVIRONMENT")


def get_settings() -> Settings:
    return Settings()