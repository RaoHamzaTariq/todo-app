"""
Environment validation and settings for the Todo Application.
"""

import os
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable validation."""

    # Application
    app_name: str = "Todo API"
    environment: str = Field(default="development", validation_alias="ENVIRONMENT")

    # Database
    database_url: str = Field(..., validation_alias="DATABASE_URL")

    # Authentication
    better_auth_secret: str = Field(..., validation_alias="BETTER_AUTH_SECRET")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    access_token_expire_days: int = Field(default=7, validation_alias="ACCESS_TOKEN_EXPIRE_DAYS")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        validation_alias="CORS_ORIGINS"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment == "production"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Create settings instance
settings = get_settings()
