from tkinter import EW, NS
from tkinter import Toplevel

from pages.ContainerSwitch.widgets.buttons import SwitchButtons
from pages.ContainerSwitch.widgets.containers_reels import ContainersReels
from pages.ContainerSwitch.widgets.switch_info import SwitchInfo
from utils.tk_windows import terminate, window_size


class ContainerSwitch(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.protocol("WM_DELETE_WINDOW", lambda: terminate(self))
        self.initialize(parent)
        self.win_config()
        self.add_widgets()
        # To ensure window stays on top and focused
        self.grab_set()
        self.mainloop()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.res = False

    def win_config(self):
        self.title("Switch Containers")
        self.config(bg="lightgrey", bd=20)
        self.win_size = window_size(self)
        self.win_size["width"] = int(self.win_size["w_screen"] / 2)
        self.win_size["height"] = int(self.win_size["h_screen"] * 4 / 5)
        x_position = int(self.win_size["w_screen"] / 4)
        y_position = int(self.win_size["h_screen"] / 25)
        self.geometry(
            f"{self.win_size['width']}x{self.win_size['height']}+{x_position}+{y_position}"
        )
        self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=25, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")

    def add_widgets(self):

        self.widgets["switch_info"] = SwitchInfo(self)
        self.widgets["switch_info"].grid(row=0, column=1, sticky=NS + EW)

        self.widgets["containers_reels"] = ContainersReels(self)
        self.widgets["containers_reels"].grid(row=1, column=1, pady=10, sticky=NS + EW)

        self.widgets["switch_buttons"] = SwitchButtons(self)
        self.widgets["switch_buttons"].grid(row=4, column=1, sticky=EW)
