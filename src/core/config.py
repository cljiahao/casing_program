from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings(BaseSettings):
    """Base settings configuration."""

    __config__ = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )


class CommonSettings(Settings):
    """Common settings for the application."""

    PROJECT_NAME: str = Field(default="My Project")
    PROJECT_VERSION: str = Field(default="v1.0.0")
    ENV_STAGE: str = Field(default="stage")


class DatabaseSettings(Settings):
    """Database configuration settings."""

    DB_NAME: str = Field(default="local")
    ADMIN_MESID: str = Field(default="")


class ServiceSettings(Settings):
    """Service-specific settings."""

    ROB_API_KEY: str = Field(default="")

    PMSS_API_URL: str = Field(default="")
    CM_API_URL: str = Field(default="")


# Instantiate settings
common_settings = CommonSettings()
service_settings = ServiceSettings()
database_settings = DatabaseSettings()
