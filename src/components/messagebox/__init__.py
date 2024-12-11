from tkinter import EW
from tkinter import Toplevel

from components.messagebox.constant import messagebox_info
from components.messagebox.widgets.buttons import CustomMessageBoxButtons
from components.messagebox.widgets.messagebox_content import CustomMessageBoxContent
from utils.tk_windows import terminate, window_size


class CustomMessageBox(Toplevel):
    def __init__(self, parent, title: str, message: str, mode: str):
        super().__init__(parent)
        self.protocol("WM_DELETE_WINDOW", lambda: terminate(self))
        self.initialize(parent, mode)
        self.win_config(title)
        self.add_widgets(message)
        # To ensure window stays on top and focused
        self.grab_set()
        self.mainloop()

    def initialize(self, parent, mode: str):
        self.parent = parent
        self.widgets = {}
        self.res = False
        if mode not in messagebox_info:
            raise ValueError(f"{mode} not part of known modes")
        self.msgbox_mode = messagebox_info[mode]

    def win_config(self, title: str):
        self.title(title)
        self.config(bg=self.msgbox_mode["bg_color"])
        self.win_size = window_size(self)
        self.win_size["width"] = int(self.win_size["w_screen"] / 3)
        self.win_size["height"] = int(self.win_size["h_screen"] / 4)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 3)
        self.geometry(
            f"{self.win_size['width']}x{self.win_size['height']}+{x_position}+{y_position}"
        )
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform="a")
        self.rowconfigure(0, weight=5, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")

    def add_widgets(self, message: str):
        custom_msgbox_content = CustomMessageBoxContent(self, message)
        custom_msgbox_content.grid(row=0, column=0, columnspan=2, sticky=EW)

        custom_msgbox_buttons = CustomMessageBoxButtons(self)
        custom_msgbox_buttons.grid(row=1, column=1, sticky=EW)
