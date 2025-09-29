from tkinter import EW, NS
from tkinter import Entry, Frame, Label, StringVar, Tk, Toplevel


class LabelEntry(Frame):
    """
    Tkinter Frame holding a label and entry.

    Args:
        parent: Toplevel to place the frame into.
        label: Label string to show what the entry is for.
        font_size: Font size for both label and entry.
        toColumn: A boolean flag to trigger label entry in a row or column format.
    """

    def __init__(
        self,
        parent: Toplevel,
        label: str,
        font_size: tuple[str, str] | tuple[str, str, str],
        toColumn: bool = False,
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.cache: dict[str, StringVar] = {"entry": StringVar(value="")}
        self.win_config(toColumn)
        self.add_widgets(label, font_size, toColumn)

    def win_config(self, toColumn: bool) -> None:
        self.rowconfigure(0, weight=1, uniform="a")
        if toColumn:
            self.rowconfigure(1, weight=1, uniform="a")
        self.columnconfigure(0, weight=1, uniform="a")
        if not toColumn:
            self.columnconfigure(1, weight=1, uniform="a")

    def add_widgets(
        self,
        label: str,
        font_size: tuple[str, str] | tuple[str, str, str],
        toColumn: bool,
    ) -> None:

        entry_row = 0
        entry_col = 1
        if toColumn:
            entry_row = 1
            entry_col = 0

        Label(self, text=label, font=font_size).grid(
            row=0, column=0, ipadx=10, ipady=10, sticky=NS + EW
        )
        Entry(self, textvariable=self.cache["entry"], font=font_size).grid(
            row=entry_row, column=entry_col, padx=5, pady=5, sticky=NS + EW
        )
