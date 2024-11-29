import json
import logging
import logging.config
import logging.handlers
from pathlib import Path
from datetime import datetime as dt

from core.config import common_settings
from core.directory import directory


class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """Custom log handler that rotates log files daily and organizes them by month."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.namer = self.change_name

    def change_name(self, default_name: str) -> str:
        """Change the log filename to include the current month and year."""
        file_path = Path(default_name)
        tail = file_path.name

        # Ensure log directory and subdirectories exist
        mth_fol = directory.log_dir / dt.now().strftime("%b%Y")
        mth_fol.mkdir(parents=True, exist_ok=True)

        # Construct new filename with the month-year prefix
        arr = tail.split(".")
        ext = arr.pop()
        fname = "_".join(arr) + f".{ext}"

        return str(mth_fol / fname)


# Register the custom handler
logging.handlers.MyTimedRotatingFileHandler = MyTimedRotatingFileHandler


def setup_logging() -> None:
    """Set up logging configuration from a JSON file or default settings."""
    logging_config_path = Path(__file__).parent / "json" / "logging.json"
    if logging_config_path.exists():
        with logging_config_path.open("rt") as f:
            config = json.load(f)
        # Update file paths in the logging configuration
        handlers = config.get("handlers", {})
        for handler_config in handlers.values():
            filename = handler_config.get("filename")
            if filename:
                handler_config["filename"] = str(directory.log_dir / filename)

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


# Setup logging and create logger instance
setup_logging()
logger = logging.getLogger(common_settings.ENV_STAGE)
