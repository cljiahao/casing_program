from tkinter import EW, NS
from tkinter import Button, Frame

from pages.ContainerScan.utils.buttons import end_lot, refresh, clear, switch


class ScanButtons(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.button_info = {
            "clear": {
                "text": "Clear",
                "onClick": clear,
                "bg": "black",
                "fg": "whitesmoke",
                "font": ("Calibri", "14", "bold"),
            },
            "switch": {
                "text": "Switch",
                "onClick": switch,
                "bg": "royalblue1",
                "fg": "whitesmoke",
                "font": ("Calibri", "14", "bold"),
            },
            "refresh": {
                "text": "Refresh",
                "onClick": refresh,
                "bg": "palegreen",
                "fg": "black",
                "font": ("Calibri", "14"),
            },
            "lotend": {
                "text": "Lot End",
                "onClick": end_lot,
                "bg": "firebrick2",
                "fg": "whitesmoke",
                "font": ("Calibri", "14", "bold"),
            },
        }

    def win_config(self):
        self.rowconfigure(0, weight=1)
        for i in range(len(self.button_info)):
            self.columnconfigure(i, weight=1, uniform="a")

    def add_widgets(self):

        for j, value in enumerate(self.button_info.values()):
            button = Button(
                self,
                text=value["text"],
                font=value["font"],
                bg=value["bg"],
                fg=value["fg"],
            )
            button.grid(row=0, column=j, padx=10, pady=10, sticky=NS + EW)
            if callable(value["onClick"]):
                button.configure(
                    command=lambda value=value: value["onClick"](self.parent)
                )
