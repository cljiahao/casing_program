from tkinter import Button, Frame

from core.constants import font_size
from pages.ContainerSwitch.utils.buttons import update_db
from utils.tk_windows import terminate


class SwitchButtons(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        self.config(bg="lightgrey")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")

    def add_widgets(self):
        Button(
            self,
            text="Cancel",
            bg="firebrick2",
            fg="whitesmoke",
            font=(*font_size["M"], "bold"),
            command=lambda: terminate(self.parent),
        ).grid(row=0, column=0, ipady=2)
        Button(
            self,
            text="Confirm",
            bg="palegreen",
            font=font_size["M"],
            command=lambda: update_db(self.parent),
        ).grid(row=0, column=1, ipady=2)
