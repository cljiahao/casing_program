from tkinter import EW, NS
from tkinter import Frame, Label, OptionMenu, StringVar, Toplevel


class LabelDropdown(Frame):
    """
    Tkinter Frame holding a label and dropdown box.

    Args:
        parent: Toplevel to place the frame into.
        option: List of strings to show in the dropdown box.
        label: Optional label string to show what the dropdown box is.
        value: Value placeholder to show on dropdown box.
    """

    def __init__(
        self,
        parent: Toplevel,
        option: list[str],
        label: str = "",
        value: str = "Choose 1",
    ) -> None:
        super().__init__(parent)
        self.initialize(parent, value or option[0])
        self.win_config()
        self.add_widgets(label, option)

    def initialize(self, parent, value) -> None:
        self.parent = parent
        self.selection = StringVar(value=value)

    def win_config(self) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=2, uniform="a")

    def add_widgets(self, label, option) -> None:

        drop_col = 0
        drop_col_span = 2
        if label:
            Label(self, text=label).grid(row=0, column=0, sticky=NS + EW)
            drop_col = drop_col_span = 1

        option = OptionMenu(self, self.selection, *option)
        option.grid(row=0, column=drop_col, columnspan=drop_col_span, sticky=NS + EW)
