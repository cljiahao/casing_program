from tkinter import EW
from tkinter import Frame, Label

from core.constants import font_size
from core.directory import directory
from utils.tk_windows import image_resize


class CustomMessageBoxContent(Frame):
    def __init__(self, parent, message: str):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets(message)

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.logo = image_resize(
            directory.resource_path(f"assets/{parent.msgbox_mode['logo_name']}"),
            parent.win_size,
            0.5,
        )

    def win_config(self):
        self.config(bg=self.parent.msgbox_mode["bg_color"])
        for i in range(5):
            weight = 1 if i % 2 == 0 else 3 + i
            self.columnconfigure(i, weight=weight, uniform="a")

    def add_widgets(self, message: str):
        Label(self, image=self.logo, bg=self.parent.msgbox_mode["bg_color"]).grid(
            row=0, column=1, rowspan=3, sticky=EW
        )
        Label(
            self,
            text=message,
            wraplength=self.parent.win_size["width"] / 2,
            bg=self.parent.msgbox_mode["bg_color"],
            font=font_size["L"],
        ).grid(row=1, column=3, sticky=EW)
