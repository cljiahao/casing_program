from tkinter import E
from tkinter import Frame, Label

from core.config import common_settings
from core.constants import font_size
from core.directory import directory
from utils.tk_windows import image_resize


class SplashContent(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}
        self.logo = image_resize(
            directory.resource_path(f"assets/brand.png"), self.parent.win_size, 0.77
        )

    def win_config(self):
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(4, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(3, weight=1, uniform="a")

    def add_widgets(self):
        Label(self, image=self.logo).grid(row=1, column=1, columnspan=2)
        Label(self, text=common_settings.PROJECT_NAME, font=font_size["2XL"]).grid(
            row=2, column=1, columnspan=2, pady=(7, 3)
        )
        Label(self, text=common_settings.PROJECT_VERSION, font=font_size["XS"]).grid(
            row=3, column=2, sticky=E
        )
