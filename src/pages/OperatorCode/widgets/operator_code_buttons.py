import sys
from tkinter import EW, NS, RAISED
from tkinter import Button, Frame

from core.constants import font_size
from utils.tk_windows import terminate


class OperatorCodeButtons(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        self.config(bg="#DDD")

    def add_widgets(self):
        Button(
            self,
            text="Close Program",
            bg="firebrick2",
            font=font_size["M"],
            relief=RAISED,
            command=lambda: sys.exit(),
        ).grid(row=0, column=0, padx=10, pady=10, sticky=NS + EW)
