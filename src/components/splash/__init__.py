from tkinter import EW, NS, Tk

from components.splash.widgets.splash_content import SplashContent
from utils.tk_windows import window_size


class Splash(Tk):
    def __init__(self, main):
        super().__init__()
        self.initialize()
        self.win_config()
        self.add_widgets()
        # Hide title bar
        self.overrideredirect(1)
        self.after(1000, self.withdraw)
        self.after(1500, main, self)

    def initialize(self):
        self.widgets = {}

    def win_config(self):
        self.config(bg="#777", bd=0)
        self.win_size = window_size(self)
        self.win_size["width"] = int(self.win_size["w_screen"] / 3)
        self.win_size["height"] = int(self.win_size["h_screen"] / 3)
        x_position = int(self.win_size["w_screen"] / 3)
        y_position = int(self.win_size["h_screen"] / 5)
        self.geometry(
            f"{self.win_size['width']}x{self.win_size['height']}+{x_position}+{y_position}"
        )
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def add_widgets(self):

        splash_message = SplashContent(self)
        splash_message.grid(row=0, column=0, sticky=NS + EW)
