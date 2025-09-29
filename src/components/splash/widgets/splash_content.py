from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from components.splash import Splash

from tkinter import E
from tkinter import Frame, Label

from core.config import common_settings
from constants.common import font_size
from core.directory_manager import directory_manager as dm
from utils.tk_windows import image_resize


class SplashContent(Frame):
    """
    Tkinter Frame holding the image logo, program title and version.

    Args:
        parent: Splash Toplevel.
    """

    def __init__(self, parent: Splash) -> None:
        super().__init__(parent)
        self.parent = parent
        self.logo = image_resize(
            dm.resource_path(f"assets/brand.png"), self.parent.win_size, 0.77
        )
        self.title_font = (
            font_size["M"]
            if self.parent.win_size["w_screen"] < 1500
            else font_size["2XL"]
        )
        self.win_config()
        self.add_widgets()

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.rowconfigure(4, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(2, weight=1, uniform="a")

    def add_widgets(self) -> None:
        Label(self, image=self.logo).grid(row=1, column=1)
        Label(self, text=common_settings.PROJECT_NAME, font=self.title_font).grid(
            row=2, column=1, pady=(7, 3)
        )
        Label(self, text=common_settings.PROJECT_VERSION, font=font_size["XS"]).grid(
            row=3, column=1, sticky=E
        )
