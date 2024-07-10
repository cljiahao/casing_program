import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    ENV_STAGE: str = os.getenv("ENV_STAGE", "debug")
    LOCAL_DB_PATH: str = os.getenv("LOCAL_DB_PATH", "./local.db")
    ADMIN_MESID: str = os.getenv("ADMIN_MESID")

    PMSS_API_URL: str = os.getenv("PMSS_API_URL")
    CM_API_URL: str = os.getenv("CM_API_URL")

    ROB_API_KEY: str = os.getenv("ROB_API_KEY")


settings = Settings()
