from tkinter import Button, Frame

from core.constants import font_size


class CustomMessageBoxButtons(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initialize(parent)
        self.win_config()
        self.add_widgets()

    def initialize(self, parent):
        self.parent = parent
        self.widgets = {}

    def win_config(self):
        self.config(bg=self.parent.msgbox_mode["bg_color"])
        for i in range(2):
            self.columnconfigure(i, weight=1, uniform="a")

    def add_widgets(self):
        for i, text in enumerate(self.parent.msgbox_mode["button_texts"]):
            Button(
                self,
                text=text,
                font=font_size["S"],
                command=lambda text=text: self.parent.msgbox_mode["command"](
                    self.parent, text
                ),
            ).grid(row=0, column=i, ipadx=30)
