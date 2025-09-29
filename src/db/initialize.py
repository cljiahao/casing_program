import bcrypt
from sqlalchemy import func
from sqlalchemy import insert, select

from core.config import database_settings
from db.models.login import MESID, Login
from db.session import get_db


def mesid_initialize() -> None:
    """Initializes the MESID table with the admin MESID if it does not exist."""

    db = next(get_db())
    init_mesid = database_settings.ADMIN_MESID.lower()

    # Check if the MESID already exists
    mesid_exists = db.scalar(select(func.count()).where(MESID.mesid == init_mesid))

    if not mesid_exists:
        # Insert the initial MESID if it does not exist
        db.execute(insert(MESID), {"mesid": init_mesid})
        db.commit()

    init_username = database_settings.ADMIN_USERNAME
    init_password = database_settings.ADMIN_PASSWORD
    pwd = init_password.encode()
    salt = bcrypt.gensalt()

    admin_exists = db.scalar(select(func.count()).where(Login.user == init_username))
    if not admin_exists:
        db.execute(
            insert(Login), {"user": init_username, "password": bcrypt.hashpw(pwd, salt)}
        )
        db.commit()
