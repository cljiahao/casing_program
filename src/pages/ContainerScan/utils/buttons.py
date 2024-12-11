from components.messagebox import CustomMessageBox
from db.repository.casing import (
    delete_reel_data,
    get_cont_scan_reels,
)
from db.session import get_db
from pages.ContainerSwitch import ContainerSwitch
from pages.Login import Login
from utils.api_utils import check_lot_exists, check_set_lot_data, set_cont_not_empty
from utils.db_utils import reel_validation
from utils.error_handler import handle_exceptions
from utils.tk_helper import refresh_container_widget, refresh_reel_count_widget
from utils.tk_windows import clear_value


def clear(parent) -> None:
    """Clears specific cache values in the parent GUI."""

    for key in parent.cache.keys():
        if key.lower() not in ["optcode", "mcno"]:
            parent.cache[key].set("")
    refresh_container_widget(parent, "")
    parent.widgets["wos_info"].widgets["lotNo"].focus()


def switch(parent) -> None:
    """Handles the container switch operation."""

    try:
        lot_no = parent.cache["lotNo"].get()

        # Check if lot no exists in PMSS
        check_lot_exists(lot_no)

        # Login and initiate container switch
        if Login(parent, "Login to Start Container Switch").res:
            if ContainerSwitch(parent).res:
                refresh_container_widget(parent, lot_no)
                clear_value(parent.widgets["wos_info"].widgets["contid"])
    except Exception as e:
        handle_exceptions(parent, e)


def refresh(parent) -> None:
    """Refreshes the parent GUI with updated lot information."""

    try:
        lot_no = parent.cache["lotNo"].get()

        # Check if lot no exists, retrieve lot data and reel IDs from PMSS
        lot_data = check_lot_exists(lot_no)
        reel_ids = lot_data.pop("ReelID")

        # TODO: Question: Refresh need a pop up to show that it was refreshed?
        # Validate reels and update the GUI
        reel_validation(lot_no, reel_ids)
        refresh_reel_count_widget(parent, lot_no, lot_data)

    except Exception as e:
        handle_exceptions(parent, e)


def end_lot(parent):
    """Handles the process of ending a lot."""

    try:
        lot_no = parent.cache["lotNo"].get()
        opt_code = parent.cache["OptCode"].get()

        # Check if lot no exists, retrieve lot data and reel IDs from PMSS
        lot_data = check_lot_exists(lot_no)
        lot_data["OptCode"] = opt_code
        reel_ids = lot_data.pop("ReelID")

        reel_validation(lot_no, reel_ids)

        # Retrieve scanned reels and containers for the given lot
        containers = get_cont_scan_reels(next(get_db()), lot_no)

        # Prepare container and reel data for server submission
        cont_dict = {}
        for cont in containers:
            cont_dict.setdefault(cont.contid, []).append(
                {
                    "id": cont.ReelID,
                    "seq": f"{(len(cont_dict[cont.contid]) + 1) / 100:.2f}".split(".")[
                        -1
                    ],
                }
            )

        cont_arr = [
            {
                "contid": key,
                "contSeq": f"{(j + 1) / 1000:.3f}".split(".")[-1],
                "Reelid": cont_dict[key],
            }
            for j, key in enumerate(cont_dict)
        ]

        lot_data["Contid"] = cont_arr

        # Submit completed lot data to PMSS
        check_set_lot_data(lot_data)

        # Mark containers as not empty in CM
        end_lot_cont_ids = [{"nov062": cont_id} for cont_id in cont_dict.keys()]
        set_cont_not_empty(end_lot_cont_ids)

        # Remove the lot data from the database
        delete_reel_data(next(get_db()), lot_no)

        CustomMessageBox(
            parent,
            title="Lot Completed",
            message="Lot successfully completed, please continue next lot",
            mode="showinfo",
        )

        # Clear the parent GUI cache
        clear(parent)

    except Exception as e:
        handle_exceptions(parent, e)
