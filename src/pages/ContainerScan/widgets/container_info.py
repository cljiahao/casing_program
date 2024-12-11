from tkinter import EW, NS, W
from tkinter import Label, LabelFrame

from core.constants import font_size


class ContainersInfo(LabelFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            name="container",
            text="Container Information",
            font=font_size["XL"],
        )
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        for i in range(4):
            weight = 1 if i % 3 == 0 else 5 * i**3
            self.rowconfigure(i, weight=weight, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")
        self.columnconfigure(2, weight=10, uniform="a")
        self.columnconfigure(3, weight=1, uniform="a")

    def add_widgets(self):

        Label(self, text="Lot No: ", font=font_size["XL"]).grid(
            row=1, column=1, sticky=W
        )

        self.widgets["lot_no"] = Label(
            self,
            textvariable=self.parent.cache["lotNo"],
            font=font_size["XL"],
        )
        self.widgets["lot_no"].grid(row=1, column=2, sticky=W)

        self.widgets["cont_id"] = LabelFrame(
            self,
            name="cont_id",
            text="Containers",
            font=font_size["XL"],
        )
        for i in range(2):
            self.widgets["cont_id"].columnconfigure(i, weight=1)
        self.widgets["cont_id"].grid(row=2, column=1, columnspan=2, sticky=NS + EW)
