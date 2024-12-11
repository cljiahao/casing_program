from tkinter import Button, Frame, Label

from core.constants import font_size
from pages.Login.utils.login_signup import login, register


class LoginButtons(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        self.config(bg="#A4C0D6")
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform="a")
            self.rowconfigure(i, weight=1, uniform="a")

    def add_widgets(self):

        info_text = Label(self, font=font_size["L"])

        Button(
            self,
            text="Register",
            font=font_size["L"],
            command=lambda: register(self.parent, info_text),
        ).grid(row=1, column=0)

        Button(
            self,
            text="Login",
            font=font_size["L"],
            command=lambda: login(self.parent, info_text),
        ).grid(row=1, column=1)
