from db.repository.casing import check_cont_exists, delete_reel_data, get_scan_reel
from db.session import get_db


def check_state(lot_no: str, cont_id: str, in_db: bool = False) -> bool:
    """Checks the state of the container and lot, ensuring valid mapping."""

    lot_cont_exists = set(check_cont_exists(next(get_db()), cont_id))

    if not lot_cont_exists:
        if in_db:
            raise LookupError(f"Container ID: {cont_id} not found in local system")
        raise LookupError(f"Container ID: {cont_id} not found in CM")

    if len(lot_cont_exists) > 1:
        raise ValueError(f"Container: {cont_id} tied to multiple lot in database")

    if lot_no not in lot_cont_exists and in_db:
        raise ValueError(
            f"Container: {cont_id} in another lot: {''.join(map(str,lot_cont_exists))}."
        )


def reel_validation(lot_no: str, reel_ids: list) -> list[str]:
    """Validates reel data by checking missing and extra reels."""

    # Get scanned reels from database
    reels = get_scan_reel(next(get_db()), lot_no)

    # Missing reels that has not been scanned
    miss_reels = [r for r in reels if r not in reel_ids]

    # Delete extra reels that has been scanned but not in server
    extra_reels = [r for r in reel_ids if r not in reels]
    for reel in extra_reels:
        delete_reel_data(next(get_db()), reel)

    if miss_reels:
        raise ValueError(f"Reels not fully scanned. Missing {miss_reels}")

    return miss_reels
