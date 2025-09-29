from pydantic import Field
from pydantic_settings import BaseSettings


class CommonSettings(BaseSettings):
    """Common settings for the application."""

    PROJECT_NAME: str = Field(default="My Project")
    PROJECT_VERSION: str = Field(default="v1.0.0")
    ENVIRONMENT: str = Field(default="dev")


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    DB_NAME: str = Field(default="local")
    ADMIN_MESID: str = Field(default="")
    ADMIN_USERNAME: str = Field(default="")
    ADMIN_PASSWORD: str = Field(default="")


class ServiceSettings(BaseSettings):
    """Service-specific settings."""

    ROB_API_KEY: str = Field(default="")
    PMSS_API_URL: str = Field(default="")
    CM_API_URL: str = Field(default="")


# Instantiate settings
common_settings = CommonSettings()
database_settings = DatabaseSettings()
service_settings = ServiceSettings()

print(common_settings.PROJECT_NAME)
