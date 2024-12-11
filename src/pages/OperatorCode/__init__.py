from tkinter import Toplevel

from pages.OperatorCode.widgets.operator_code_info import OperatorCodeInfo
from utils.tk_windows import terminate, window_size


class OperatorCode(Toplevel):
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
        self.title("Operator Code")
        self.config(bg="#DDD", bd=10)
        self.win_size = window_size(self)
        self.win_size["width"] = int(self.win_size["w_screen"] / 3)
        self.win_size["height"] = int(self.win_size["h_screen"] / 5)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 35)
        self.geometry(
            f"{self.win_size['width']}x{self.win_size['height']}+{x_position}+{y_position}"
        )
        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=1)

    def add_widgets(self):
        self.widgets["optcode_info"] = OperatorCodeInfo(self)
        self.widgets["optcode_info"].grid(row=1, column=1)
