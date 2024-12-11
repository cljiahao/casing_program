from tkinter import CENTER, EW, NS, W
from tkinter import Entry, Frame, Label

from core.constants import font_size


class ReelScan(Frame):
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
        self.columnconfigure(1, weight=3, uniform="a")

    def add_widgets(self):
        Label(
            self,
            text=f"Reel ID",
            bg="lightgrey",
            font=font_size["M"],
        ).grid(row=0, column=0, sticky=W)

        self.widgets["reel"] = Entry(
            self,
            name="reel",
            font=font_size["M"],
            justify=CENTER,
            validate="key",
            validatecommand=self.parent.reg_entry,
        )
        self.widgets["reel"].grid(row=0, column=1, ipady=3, sticky=NS + EW)
