from tkinter import EW, LEFT, RAISED
from tkinter import Frame, Label

from core.constants import font_size


class ErrorInfo(Frame):
    def __init__(self, parent, error: str):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets(error)

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        self.config(bg="#A4C0D6", bd=10)
        self.columnconfigure(0, weight=1)

    def add_widgets(self, error):
        error = error if len(error) < 200 else f"{error[0:200]} ..."
        Label(
            self,
            text=error,
            wraplength=500,
            bg="#FFF",
            fg="#CF352E",
            font=(*font_size["L"], "bold"),
            relief=RAISED,
            justify=LEFT,
        ).grid(row=0, column=0, ipady=15, sticky=EW)
