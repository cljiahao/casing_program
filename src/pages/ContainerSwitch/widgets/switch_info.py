from tkinter import EW, NS, RAISED
from tkinter import Frame, Label

from core.constants import font_size


class SwitchInfo(Frame):
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

    def add_widgets(self):
        self.widgets["info"] = Label(
            self,
            text="Scan old and new containers below to transfer",
            bg="lightgrey",
            font=font_size["L"],
            relief=RAISED,
        )
        self.widgets["info"].grid(
            row=0, column=0, pady=5, ipady=10, ipadx=10, sticky=NS + EW
        )
