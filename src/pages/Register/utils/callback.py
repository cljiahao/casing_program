from core.logging import logger
from db.repository.login import retrieve_mesid
from db.session import get_db
from utils.tk_windows import clear_value, terminate


def callback(parent, prompt: str, name: str) -> bool:
    """Handles the callback logic for checking entries and invoking corresponding handlers."""

    key_name = name.split(".")[-1]
    return entry_match(parent, prompt, key_name)


def entry_match(parent, prompt: str, key_name: str) -> bool:
    """Routes entry processing based on the key name."""

    prompt_length = len(prompt)
    match key_name:
        case "mesid":
            return handle_mesid_entry(parent, prompt, prompt_length, key_name)


def handle_mesid_entry(parent, prompt: str, prompt_length: int, key_name: str) -> bool:
    """Handles the processing of the mesid entry."""

    if prompt_length > 8:
        return False
    if prompt_length == 8:
        logger.info("%s scanned to authorize", prompt)
        parent.res = retrieve_mesid(next(get_db()), prompt.lower())
        if parent.res:
            terminate(parent)
        else:
            # Clear the value of the widget matching the key
            key = next(
                (k for k in parent.widgets.keys() if k.lower() == key_name), None
            )
            if key:
                clear_value(parent.widgets[key])

    return True
