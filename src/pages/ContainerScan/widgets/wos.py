from tkinter import CENTER, W
from tkinter import Button, Entry, Label, LabelFrame

from core.constants import font_size, wos_labels
from pages.ContainerScan.utils.callback import callback
from utils.tk_windows import clear_value


class WOSInfo(LabelFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            name="wos",
            text="WOS Information (Lot Key In)",
            font=font_size["XL"],
        )
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        self.rowconfigure(0, weight=5, uniform="a")
        for i in range(len(wos_labels)):
            self.rowconfigure(i + 1, weight=3, uniform="a")
        self.rowconfigure(len(wos_labels) + 1, weight=5, uniform="a")
        for i in range(4):
            weight = 1 if i % 3 == 0 else i * 2
            self.columnconfigure(i, weight=weight, uniform="a")
        self.reg_entry = (
            self.register(lambda input, name: callback(self, input, name)),
            "%P",
            "%W",
        )

    def add_widgets(self):
        for i, labels in enumerate(wos_labels):

            key = labels["key"]

            Label(self, text=f"{labels['name']}: ", font=font_size["XL"]).grid(
                row=i + 1, column=1, ipadx=5, ipady=5, padx=5, sticky=W
            )

            if labels["type"] == "entry":
                self.widgets[key] = Entry(
                    self,
                    name=key.lower(),
                    textvariable=self.parent.cache[key],
                    font=font_size["XL"],
                    justify=CENTER,
                    validate="key",
                    validatecommand=self.reg_entry,
                )

                Button(
                    self,
                    text="x",
                    width=2,
                    bg="#fa6565",
                    font=font_size["S"],
                    command=lambda k=key: clear_value(self.widgets[k]),
                ).grid(row=i + 1, column=3, sticky=W)

            elif labels["type"] == "label":
                self.widgets[key] = Label(
                    self,
                    textvariable=self.parent.cache[key],
                    font=font_size["XL"],
                    width=50,
                    anchor=W,
                )

            self.widgets[key].grid(
                row=i + 1, column=2, ipadx=5, ipady=5, padx=10, sticky=W
            )

        self.widgets[
            next(
                (label["key"] for label in wos_labels if label.get("type") == "entry"),
                None,
            )
        ].focus()
