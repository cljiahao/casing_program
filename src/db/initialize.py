from sqlalchemy import func
from sqlalchemy import insert, select

from core.config import settings
from db.models.login import MESID
from db.session import get_db


def db_initialize():
    db = next(get_db())
    mesid_exists = db.scalar(
        select(func.count()).where(MESID.mesid == settings.ADMIN_MESID)
    )

    if not mesid_exists:
        db.execute(insert(MESID), {"mesid": settings.ADMIN_MESID})
        db.commit()
