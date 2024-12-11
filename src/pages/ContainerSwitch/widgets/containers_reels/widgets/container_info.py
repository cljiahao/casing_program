from tkinter import CENTER, EW, NS
from tkinter import Entry, Frame, Label, LabelFrame


from core.constants import font_size


class ContainerInfo(Frame):
    def __init__(self, parent, mode: str):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets(mode)

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        self.config(bg="lightgrey")
        self.rowconfigure(1, weight=1, uniform="a")
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform="a")

    def add_widgets(self, mode: str):
        Label(
            self, text=f"Container [{mode}]", bg="lightgrey", font=font_size["M"]
        ).grid(row=0, column=0, padx=(0, 5), sticky=EW)

        self.widgets["contid"] = Entry(
            self,
            name=mode.lower(),
            font=font_size["M"],
            justify=CENTER,
            validate="key",
            validatecommand=self.parent.reg_entry,
        )

        self.widgets["contid"].grid(row=0, column=1)

        self.widgets["reelids"] = LabelFrame(
            self,
            text=" ",
            font=font_size["XL"],
        )
        self.widgets["reelids"].columnconfigure(0, weight=1)
        self.widgets["reelids"].columnconfigure(1, weight=1)
        self.widgets["reelids"].grid(
            row=1, column=0, columnspan=2, pady=10, sticky=NS + EW
        )
