from core.logging import logger

# from db.session import get_db
from utils.tk_windows import terminate


def callback(parent, prompt: str, name: str) -> bool:
    """Handles the callback logic for checking entries and invoking corresponding handlers."""

    key_name = name.split(".")[-1]
    return entry_match(parent, prompt, key_name)


# TODO: callback for checking optcode if exists in operator system


def entry_match(parent, prompt: str, key_name: str) -> bool:
    """Routes entry processing based on the key name."""

    prompt_length = len(prompt)
    match key_name:
        case "optcode":
            return handle_optcode_entry(parent, prompt, prompt_length)


def handle_optcode_entry(parent, prompt: str, prompt_length: int) -> bool:
    """Handles the processing of the optcode entry."""

    if prompt_length > 7:
        return False
    if prompt_length == 7:
        logger.info("%s scanned to start casing operation", prompt)
        parent.parent.cache["OptCode"].set(prompt)
        parent.res = True
        terminate(parent)

    return True
