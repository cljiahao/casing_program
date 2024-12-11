from tkinter import EW, NS
from tkinter import Frame

from pages.ContainerSwitch.utils.callback import callback
from pages.ContainerSwitch.widgets.containers_reels.widgets.container_info import (
    ContainerInfo,
)
from pages.ContainerSwitch.widgets.containers_reels.widgets.reel_scan import ReelScan


class ContainersReels(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.cache = {"Old": [], "New": []}

    def win_config(self):
        self.config(bg="lightgrey")
        self.rowconfigure(0, weight=1, uniform="a")
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform="a")
        self.reg_entry = (
            self.register(lambda input, name: callback(self, input, name)),
            "%P",
            "%W",
        )

    def add_widgets(self):

        for i, mode in enumerate(self.cache.keys()):
            self.widgets[f"{mode.lower()}_container"] = ContainerInfo(self, mode)
            self.widgets[f"{mode.lower()}_container"].grid(
                row=0, column=i, padx=10, pady=5, sticky=NS + EW
            )

        self.widgets["reel_scan"] = ReelScan(self)
        self.widgets["reel_scan"].grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky=NS + EW
        )
