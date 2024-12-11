from tkinter import EW
from tkinter import Entry, Frame, Label

from core.constants import font_size


class MESIDLogin(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.labels = [
            {"key": "mesid", "text": "MES ID"},
            {"key": "user", "text": "Username"},
            {"key": "pwd", "text": "Password"},
        ]

    def win_config(self):
        self.config(bg="#A4C0D6", bd=10)
        for i in range(4):
            self.rowconfigure(i, weight=1, uniform="a")
        for i in range(4):
            weight = 1 if i % 3 == 0 else i + 1
            self.columnconfigure(i, weight=weight, uniform="a")

    def add_widgets(self):

        Label(self, text="OR", bg="#A4C0D6", font=(*font_size["L"], "bold")).grid(
            row=1, column=1, columnspan=2, pady=10
        )

        for i, label in enumerate(self.labels):
            row = i + 1 if i > 0 else 0
            Label(self, text=label["text"], bg="#A4C0D6", font=font_size["L"]).grid(
                row=row, column=1
            )
            self.widgets[label["key"]] = Entry(self, font=font_size["L"])
            self.widgets[label["key"]].grid(row=row, column=2, sticky=EW)

        self.widgets["pwd"].config(show="*")
        self.widgets["mesid"].focus()
