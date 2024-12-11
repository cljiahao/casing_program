from core.logging import logger
from pages.Login import Login
from utils.tk_windows import loop_till_approve


def handle_exceptions(parent, e: Exception) -> None:
    """Handles exceptions by logging and showing the error in the UI."""

    logger.error(e, exc_info=True)
    loop_till_approve(Login, parent, e.__str__())


def update_label_exceptions(widget, text: str, bg: str) -> None:
    """Updates the widget label with the provided text and background color."""

    if widget.cget("bg") != bg:
        widget.config(text=text, bg=bg)

        if bg == "tomato":
            logger.error(text, exc_info=True)
        elif bg == "palegreen":
            logger.info(text)
