from pages.ContainerScan.utils.casing import run_cont_id, run_lot_no, run_reel_id
from utils.error_handler import handle_exceptions
from utils.tk_windows import clear_value


def callback(parent, prompt: str, name: str) -> bool:
    """Callback function to handle entry inputs and match them to the appropriate handler."""

    try:
        key_name = name.split(".")[-1]
        return entry_match(parent, prompt, key_name)
    except Exception as e:
        handle_exceptions(parent, e)
        # Clear the value of the widget matching the key
        key = next((k for k in parent.widgets.keys() if k.lower() == key_name), None)
        if key:
            clear_value(parent.widgets[key])
        return True


def entry_match(parent, prompt: str, key_name: str) -> bool:
    """Matches the key_name to its corresponding handler function."""

    prompt_length = len(prompt)

    match key_name:
        # case "optcode":
        #     handle_optcode_entry(parent, prompt, prompt_length)
        case "lotno":
            return handle_lotno_entry(parent, prompt, prompt_length)
        case "contid":
            return handle_contid_entry(parent, prompt, prompt_length)
        case "reelid":
            return handle_reelid_entry(parent, prompt, prompt_length)

    return True


# def handle_optcode_entry(parent, prompt: str, prompt_length: int) -> bool:
#   """Handles the optcode input, including validations and updating widgets."""

#     if prompt_length > 7:
#         return False
#     if prompt_length == 7:
#         parent.widgets["lotNo"].focus()

#     return True


def handle_lotno_entry(parent, prompt: str, prompt_length: int) -> bool:
    """Handles the lot number input, including validations and updating widgets."""

    grandparent = parent.parent

    if grandparent.cache["OptCode"].get() == "":
        raise ValueError("Please Scan Operator ID First")
    if prompt_length > 10:
        return False

    # Update background color based on input length
    bg_color = "red" if 0 < prompt_length < 10 else "gray94"
    if prompt_length == 10:
        grandparent.reel_per_box, grandparent.reel_ids = run_lot_no(grandparent, prompt)
        parent.widgets["contid"].focus()

    grandparent.widgets["cont_info"].widgets["lot_no"].config(bg=bg_color)

    return True


def handle_contid_entry(parent, prompt: str, prompt_length: int) -> bool:
    """Handles the container ID input, including validations and updating focus."""

    grandparent = parent.parent

    if prompt_length > 10:
        return False
    if prompt_length == 10:
        run_cont_id(grandparent, prompt)
        parent.widgets["Reelid"].focus()

    return True


def handle_reelid_entry(parent, prompt: str, prompt_length: int) -> bool:
    """Handles the reel ID input, including validations and refreshing the container widget."""

    grandparent = parent.parent

    if prompt_length > 15:
        return False
    if prompt_length == 15:
        cont_full = run_reel_id(grandparent, prompt)
        # Clear and refocus reel ID
        clear_value(parent.widgets["Reelid"])
        if cont_full:
            # Clear and refocus container ID
            clear_value(parent.widgets["contid"])

    return True
