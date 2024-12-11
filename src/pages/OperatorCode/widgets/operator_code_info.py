from tkinter import EW, RAISED
from tkinter import Entry, Frame, Label

from core.constants import font_size
from pages.OperatorCode.utils.callback import callback


class OperatorCodeInfo(Frame):
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
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(3, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(1, weight=1, uniform="a")
        self.reg_entry = (
            self.register(lambda input, name: callback(self.parent, input, name)),
            "%P",
            "%W",
        )

    def add_widgets(self):
        Label(
            self,
            text="Please scan Operator ID to start Casing program",
            bg="#FFF",
            fg="#CF352E",
            font=(*font_size["L"], "bold"),
            relief=RAISED,
        ).grid(row=0, column=1, columnspan=2, pady=10, ipady=7, ipadx=5, sticky=EW)

        # MES ID
        Label(self, text="MES ID:", bg="#DDD", font=font_size["L"]).grid(
            row=1, column=1
        )
        self.widgets["optcode"] = Entry(
            self,
            name="optcode",
            font=font_size["L"],
            validate="key",
            validatecommand=self.reg_entry,
        )
        self.widgets["optcode"].grid(row=1, column=2, ipady=3, ipadx=20, pady=3)

        self.widgets["optcode"].focus()
