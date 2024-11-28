from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import database_settings
from core.directory import directory

# Database URL configuration
DB_NAME = f"{database_settings.DB_NAME}.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{directory.config_dir}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
