from tkinter import EW, NS
from tkinter import Toplevel

from pages.Login.widgets.buttons import LoginButtons
from pages.Login.widgets.error_info import ErrorInfo
from pages.Login.widgets.mesid_login import MESIDLogin
from utils.tk_windows import terminate, window_size


class Login(Toplevel):
    def __init__(self, parent, error: str):
        super().__init__(parent)
        self.protocol("WM_DELETE_WINDOW", lambda: terminate(self))
        self.initialize(parent)
        self.win_config()
        self.add_widgets(error)
        # To ensure window stays on top and focused
        self.grab_set()
        self.mainloop()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.res = False

    def win_config(self):
        self.title("Login")
        self.config(bg="#A4C0D6", bd=20)
        self.win_size = window_size(self)
        self.win_size["width"] = int(self.win_size["w_screen"] / 3)
        self.win_size["height"] = int(self.win_size["h_screen"] * 3 / 5)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 35)
        self.geometry(
            f"{self.win_size['width']}x{self.win_size['height']}+{x_position}+{y_position}"
        )
        for i in range(7):
            if i % 2 == 0:
                self.rowconfigure(i, weight=1, uniform="a")
        for i in range(3):
            weight = 1 if i % 2 == 0 else 10
            self.columnconfigure(i, weight=weight, uniform="a")

    def add_widgets(self, error: str):

        self.widgets["error_info"] = ErrorInfo(self, error)
        self.widgets["error_info"].grid(row=1, column=1, sticky=EW)

        self.widgets["mesid_login"] = MESIDLogin(self)
        self.widgets["mesid_login"].grid(row=3, column=1, sticky=EW)

        self.widgets["login_buttons"] = LoginButtons(self)
        self.widgets["login_buttons"].grid(row=5, column=1, sticky=NS + EW)
