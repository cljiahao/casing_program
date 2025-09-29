from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.messagebox import CustomMessageBox


def ask_yes_no(parent: CustomMessageBox, button_text: str):
    """Set the response based on the button text and terminate the window."""

    parent.res = button_text.lower() == "yes"
    parent.destroy()


def show_(parent: CustomMessageBox, *args):
    """Terminate the window."""

    parent.destroy()


button_map = {
    "show": show_,
    "askyesno": ask_yes_no,
}
