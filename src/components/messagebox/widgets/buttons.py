from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.messagebox import CustomMessageBox

from tkinter import Button, Frame

from constants.common import font_size
from components.messagebox.utils.buttons import button_map


class CustomMessageBoxButtons(Frame):
    """
    Tkinter Frame holding buttons for CustomMessageBox component

    Args:
        parent: CustomMessageBox Toplevel.
    """

    def __init__(self, parent: CustomMessageBox) -> None:
        super().__init__(parent)
        self.parent = parent
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.config(bg=self.parent.msgbox_mode["bg"])
        self.rowconfigure(0, weight=1, uniform="a")
        for i in range(len(self.parent.msgbox_mode["button_texts"])):
            self.columnconfigure(i, weight=1, uniform="a")

    def add_widgets(self) -> None:
        for i, text in enumerate(self.parent.msgbox_mode["button_texts"]):
            button_key = self.parent.msgbox_mode["button_key"]
            button_func = lambda text=text: button_map[button_key](self.parent, text)
            Button(self, text=text, font=font_size["S"], command=button_func).grid(
                row=0, column=i, padx=5, pady=5, ipadx=30
            )
