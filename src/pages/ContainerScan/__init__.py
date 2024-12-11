from tkinter import EW, NS
from tkinter import StringVar, Toplevel

from core.constants import wos_labels

from pages.ContainerScan.widgets.buttons import ScanButtons
from pages.ContainerScan.widgets.container_info import ContainersInfo
from pages.ContainerScan.widgets.wos import WOSInfo
from utils.tk_windows import terminate, window_size


class ContainerScan(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.protocol("WM_DELETE_WINDOW", lambda: terminate(self))
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.cache = {
            labels["key"]: StringVar(value=labels["value"]) for labels in wos_labels
        }

    def win_config(self):
        self.title("Casing Scan")
        self.state("zoomed")
        self.win_size = window_size(self)
        self.rowconfigure(0, weight=20, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")
        for i in range(5):
            weight = 1 if i % 2 == 0 else 10
            self.columnconfigure(i, weight=weight, uniform="a")
        self.columnconfigure(1, weight=17, uniform="a")

    def add_widgets(self):
        self.widgets["wos_info"] = WOSInfo(self)
        self.widgets["wos_info"].grid(row=0, column=1, rowspan=2, sticky=NS + EW)

        self.widgets["cont_info"] = ContainersInfo(self)
        self.widgets["cont_info"].grid(row=0, column=3, sticky=NS + EW)

        self.widgets["scan_buttons"] = ScanButtons(self)
        self.widgets["scan_buttons"].grid(row=1, column=3, sticky=NS + EW)
