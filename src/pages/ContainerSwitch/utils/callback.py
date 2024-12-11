from db.repository.casing import get_scan_reel_data
from db.session import get_db
from pages.ContainerSwitch.utils.switching import refresh_reel_frame
from utils.db_utils import check_state
from utils.error_handler import update_label_exceptions
from utils.tk_helper import reset_container
from utils.tk_windows import clear_value


def callback(parent, prompt: str, name: str) -> bool:
    """Handles the callback logic for container or reel entries."""

    grandparent = parent.parent
    info_widget = grandparent.widgets["switch_info"].widgets["info"]
    try:
        key_name = name.split(".")[-1]
        update_label_exceptions(info_widget, "Please continue", "lightgrey")
        return entry_match(parent, prompt, key_name)
    except Exception as e:
        update_label_exceptions(info_widget, e.__str__(), "tomato")
        return True


def entry_match(parent, prompt: str, key_name: str) -> bool:
    """Routes entry processing based on the key name."""

    prompt_length = len(prompt)
    match key_name:
        case "old" | "new":
            return handle_container_entry(parent, prompt, prompt_length, key_name)
        case "reel":
            return handle_reel_entry(parent, prompt, prompt_length)


def handle_container_entry(parent, prompt: str, prompt_length: int, mode: str) -> bool:
    """Processes entries for 'old' or 'new' containers."""

    if prompt_length > 10:
        return False
    if prompt_length == 10:
        parent.widgets[f"{mode}_container"].widgets["reelids"].config(text=prompt)
        greatgrandparent = parent.parent.parent
        lot_no = greatgrandparent.cache["lotNo"].get()

        if mode == "old":
            # Check if cont_id exists and same as lot input in database
            check_state(lot_no, prompt, True)
            parent.widgets["new_container"].widgets["contid"].focus()
        elif mode == "new":
            reset_container(parent, prompt)
            parent.widgets["reel_scan"].widgets["reel"].focus()

        # Cache and refresh reel data
        db_session = next(get_db())
        reel_data = get_scan_reel_data(db_session, lot_no, prompt)
        parent.cache[mode.capitalize()] = reel_data
        refresh_reel_frame(parent, mode)

    return True


def handle_reel_entry(parent, prompt: str, prompt_length: int) -> bool:
    """Processes reel entries."""

    if prompt_length > 15:
        return False
    if prompt_length == 15:
        greatgrandparent = parent.parent.parent
        lot_no = greatgrandparent.cache["lotNo"].get()
        old_cont_id = parent.widgets["old_container"].widgets["contid"].get()
        new_cont_id = parent.widgets["new_container"].widgets["contid"].get()

        # Check if cont_id exists and same as lot input in database
        check_state(lot_no, old_cont_id, True)

        old_reel_ids = [reel_data.ReelID for reel_data in parent.cache["Old"]]

        if prompt not in old_reel_ids:
            raise ValueError(f"ReelID: {prompt} not found in {old_cont_id}")

        reel_data = parent.cache["Old"].pop(old_reel_ids.index(prompt))
        reel_data.contid = new_cont_id
        parent.cache["New"].append(reel_data)

        refresh_reel_frame(parent, "old")
        refresh_reel_frame(parent, "new")
        clear_value(parent.widgets["reel_scan"].widgets["reel"])

    return True
