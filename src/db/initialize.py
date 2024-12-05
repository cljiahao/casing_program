from sqlalchemy import func
from sqlalchemy import insert, select

from core.config import database_settings
from db.models.login import MESID
from db.session import get_db


def db_initialize():
    db = next(get_db())
    init_mesid = database_settings.ADMIN_MESID.lower()
    mesid_exists = db.scalar(select(func.count()).where(MESID.mesid == init_mesid))

    if not mesid_exists:
        db.execute(insert(MESID), {"mesid": init_mesid})
        db.commit()
