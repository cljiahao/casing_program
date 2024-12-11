from datetime import datetime as dt
from sqlalchemy import func
from sqlalchemy import insert, select
from sqlalchemy.orm.session import Session

from core.logging import logger
from db.models.login import Login, MESID


def retrieve_mesid(db: Session, id_input: str) -> bool:
    """Check if the MESID exists in the database."""

    mesid_exists = db.scalar(select(func.count()).where(MESID.mesid == id_input))
    logger.info(
        "%s tried to authorize, authorization: %s",
        id_input,
        "Yes" if mesid_exists else "No",
    )

    db.close()

    return mesid_exists


def create_mesid(db: Session, id_input: str) -> None:
    """Create a new MESID in the database."""

    try:
        db.execute(insert(MESID), [{"date": dt.now(), "mesid": id_input}])
        db.commit()
        logger.info("%s created as authorized personnel", id_input)
    except Exception as e:
        logger.error(
            "Error creating %s as authorized personnel", id_input, exc_info=True
        )
        db.rollback()
    finally:
        db.close()


def get_login(db: Session, user_input: str) -> str:
    """Retrieve the hashed password for the given user."""

    pwd_hash = db.scalar(select(Login.password).filter(Login.user == user_input))

    db.close()

    return pwd_hash


def create_login(db: Session, user_input: str, hash_input: str) -> None:
    """Create a new login entry in the database."""

    try:
        login_data = {"user": user_input, "password": hash_input}
        login = Login(**login_data)
        db.add(login)
        db.commit()
    except Exception as e:
        logger.error("Error adding %s in database", user_input, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()
