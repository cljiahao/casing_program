from db.repository.casing import (
    check_cont_full,
    create_reel_data,
    get_cont_id_with_reel,
    get_incomplete_cont,
    get_scan_reels_cnt,
)
from db.session import get_db
from utils.api_utils import check_lot_exists
from utils.db_utils import check_state
from utils.tk_helper import (
    refresh_container_widget,
    refresh_reel_count_widget,
    reset_container,
)


def run_lot_no(root, lot_no: str) -> tuple[int, list[dict]]:
    """Processes the lot number and retrieves related data."""

    # Check if lot no exists in PMSS
    lot_data = check_lot_exists(lot_no)

    reel_per_box = int(lot_data["reelPerBox"])
    reel_ids = lot_data.pop("ReelID")

    refresh_reel_count_widget(root, lot_no, lot_data)
    refresh_container_widget(root, lot_no)

    return reel_per_box, reel_ids


def run_cont_id(root, cont_id: str) -> None:
    """Validates and processes container ID."""

    lot_no = root.cache["lotNo"].get()

    # Check if lot no exists in PMSS
    check_lot_exists(lot_no)

    # Check if cont_id exists and same as lot input in database
    check_state(lot_no, cont_id)

    # Retrieve uncomplete cont with reels below reelperbox from server
    incomplete_cont = get_incomplete_cont(next(get_db()), lot_no, root.reel_per_box)
    if incomplete_cont:
        cont_id_in_db, reel_count = incomplete_cont
        if cont_id_in_db != cont_id:
            raise ValueError(
                f"Please complete Container {cont_id_in_db} filled with {reel_count} reels",
            )

    # Check if scanning into cont more than reelperbox from server
    cont_full = check_cont_full(next(get_db()), lot_no, cont_id, root.reel_per_box)
    if cont_full:
        raise ValueError(f"Scanning more reels to full container: {cont_id}")

    # Check server if container exists and empty, reset based on input
    reset_container(root, cont_id)


def run_reel_id(root, reel_input: str) -> None:
    """Validates and processes reel ID."""

    lot_no = root.cache["lotNo"].get()
    cont_id = root.cache["contid"].get()
    reel_ids = root.reel_ids

    # Check if reel_input in reel_ids from server
    if reel_input not in reel_ids:
        raise LookupError(f"Reel: {reel_input} not found in system")

    # Check if reel scanned before into container
    cont_id_in_db = get_cont_id_with_reel(next(get_db()), lot_no, reel_input)
    if cont_id_in_db:
        raise ValueError(
            f"Reel already scanned before in {cont_id_in_db}",
        )

    # Check if cont_id exists and same as lot input in database
    check_state(lot_no, cont_id)

    # Add Reel Data into Database
    reel_data = {
        "lotNo": lot_no,
        "contid": cont_id,
        "ReelID": reel_input,
    }
    create_reel_data(next(get_db()), reel_data)

    # Get scanned reel count from database
    reel_count = get_scan_reels_cnt(next(get_db()), lot_no)
    no_of_reels = root.cache["noOfReel"].get().split(" / ")[-1]
    root.cache["noOfReel"].set(f"{reel_count} / {no_of_reels}")

    # Check if container is now reelperbox from server
    cont_full = check_cont_full(next(get_db()), lot_no, cont_id, root.reel_per_box)

    refresh_container_widget(root, lot_no)

    return cont_full
