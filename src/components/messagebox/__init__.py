from tkinter import EW, NS
from tkinter import Toplevel

from components.messagebox.constants import messagebox_info
from components.messagebox.widgets.buttons import CustomMessageBoxButtons
from components.messagebox.widgets.messagebox_content import CustomMessageBoxContent
from utils.tk_windows import window_size


class CustomMessageBox(Toplevel):
    """
    A custom Tkinter Message Box for displaying information based on the mode.

    Args:
        parent: The parent widget, usually Toplevel.
        title: Title of the Toplevel window.
        message: Message to be shown.
        mode: showinfo, showerror, showwarning, askyesno,
    """

    def __init__(self, parent: Toplevel, title: str, message: str, mode: str) -> None:
        super().__init__(parent)
        self.res = False
        if mode not in messagebox_info:
            raise ValueError(f"{mode} not part of known modes")
        self.msgbox_mode = messagebox_info[mode]
        self.win_config(title)
        self.add_widgets(message)
        # To ensure window stays on top and focused
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())
        self.grab_set()
        self.focus_set()

    def win_config(self, title: str) -> None:
        self.title(title)
        self.config(bg=self.msgbox_mode["bg"])
        self.win_size = window_size(self)
        self.win_size["width"] = int(self.win_size["w_screen"] * 0.4)
        self.win_size["height"] = int(self.win_size["h_screen"] / 3)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 4)
        self.geometry(
            f"{self.win_size['width']}x{self.win_size['height']}+{x_position}+{y_position}"
        )
        self.columnconfigure(0, weight=1, uniform="a")
        self.rowconfigure(0, weight=5, uniform="a")
        self.rowconfigure(1, weight=2, uniform="a")

    def add_widgets(self, message: str) -> None:
        CustomMessageBoxContent(self, message).grid(row=0, column=0, sticky=NS + EW)

        CustomMessageBoxButtons(self).grid(row=1, column=0, sticky=NS + EW)
