from sqlalchemy import func
from sqlalchemy import delete, select, update
from sqlalchemy.orm.session import Session

from core.logging import logger
from db.models.casing import Containers


def check_cont_exists(db: Session, cont_id: str):
    lot_cont_exists = db.scalars(
        select(Containers.lotNo).where(Containers.contid == cont_id)
    ).all()

    db.close()

    return lot_cont_exists


def check_cont_full(db: Session, lot_no: str, cont_id: str, reel_per_box: int):
    cont_full = db.scalar(
        select(func.count(Containers.ReelID))
        .where(Containers.lotNo == lot_no, Containers.contid == cont_id)
        .having(func.count(Containers.ReelID) >= reel_per_box)
    )

    db.close()

    return cont_full

def get_incomplete_cont(
    db: Session, lot_no: str, reel_per_box: int
):

    uncomplete_cont = db.execute(
        select(Containers.contid, func.count(Containers.ReelID))
        .where(Containers.lotNo == lot_no)
        .group_by(Containers.contid)
        .having(func.count(Containers.ReelID) < reel_per_box)
    ).first()

    db.close()

    return uncomplete_cont


def get_scan_reel(db: Session, lot_no: str):
    reel = db.scalars(select(Containers.ReelID).where(Containers.lotNo == lot_no)).all()

    db.close()

    return reel


def get_scan_reel_data(db: Session, lot_no: str, cont_id: str):
    reel_data = db.scalars(
        select(Containers).where(
            Containers.lotNo == lot_no, Containers.contid == cont_id
        )
    ).all()

    db.close()

    return reel_data


def get_scan_reels_cnt(db: Session, lot_no: str):
    reel_count = db.scalar(
        select(func.count(Containers.ReelID)).where(Containers.lotNo == lot_no)
    )

    db.close()

    return reel_count


def get_cont_scan_reels(db: Session, lot_no: str):
    containers = db.scalars(select(Containers).where(Containers.lotNo == lot_no)).all()

    db.close()

    return containers


def get_cont_scan_reels_cnt(db: Session, lot_no: str):
    scan_cont_reel_cnt = db.execute(
        select(Containers.contid, func.count(Containers.ReelID))
        .where(Containers.lotNo == lot_no)
        .group_by(Containers.contid)
    )

    db.close()

    return scan_cont_reel_cnt


def get_cont_id_with_reel(db: Session, lot_no: str, reel_input: str):
    cont_id = db.scalar(
        select(Containers.contid).where(
            Containers.lotNo == lot_no, Containers.ReelID == reel_input
        )
    )

    db.close()

    return cont_id


def create_reel_data(db: Session, reel_data_input: dict):
    try:
        reel_data = Containers(**reel_data_input)
        db.add(reel_data)
        db.commit()
    except Exception as e:
        logger.error("Error creating %s in database.", reel_data.lotNo, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


def update_reel_data(db: Session, reel_id: str, reel_data_input: dict):
    try:
        db.execute(
            update(Containers).where(Containers.ReelID == reel_id), reel_data_input
        )
        db.commit()
    except Exception as e:
        logger.error("Error updating %s in database.", reel_id, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()


def delete_reel_data(db: Session, lot_no: str):
    try:
        db.execute(delete(Containers).where(Containers.lotNo == lot_no))
        db.commit()
    except:
        logger.error("Error deleting %s in database.", lot_input, exc_info=True)
        db.rollback()
        raise
    finally:
        db.close()
