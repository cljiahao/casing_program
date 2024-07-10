import os
import json
import logging
import logging.handlers
import logging.config
from datetime import datetime as dt

from core.config import settings
from core.directory import directory


def change_name(default_name: str):

    _, tail = os.path.split(default_name)

    mth_fol = os.path.join(directory.log_path, dt.now().strftime("%b%Y"))
    if not os.path.exists(mth_fol):
        os.makedirs(mth_fol)

    arr = tail.split(".")
    ext = arr.pop(1)
    fname = "_".join(arr) + f".{ext}"

    new_name = os.path.join(mth_fol, fname)

    return new_name


def setup_logging():

    if os.path.exists("./core/json/logging.json"):
        with open("./core/json/logging.json", "rt") as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)


class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, **kwargs):
        logging.handlers.TimedRotatingFileHandler.__init__(self, **kwargs)
        self.namer = change_name


logging.handlers.MyTimedRotatingFileHandler = MyTimedRotatingFileHandler

setup_logging()
logger = logging.getLogger(settings.ENV_STAGE)
