from tkinter import Label, LabelFrame, Frame
from tkinter import NS, EW, E, W

from db.repository.casing import get_cont_scan_reels_cnt
from db.session import get_db


def guiCont(frame: Frame):

    cont_frame = LabelFrame(
        frame, name="container", text="Container Information", font=("Calibri", "20")
    )
    cont_frame.rowconfigure(0, weight=1, uniform="a")
    cont_frame.rowconfigure(1, weight=2, uniform="a")
    cont_frame.rowconfigure(2, weight=20, uniform="a")
    cont_frame.rowconfigure(3, weight=2, uniform="a")
    cont_frame.columnconfigure(0, weight=1, uniform="a")
    cont_frame.columnconfigure(1, weight=7, uniform="a")
    cont_frame.columnconfigure(2, weight=1, uniform="a")
    cont_frame.grid(row=0, column=3, sticky=NS + EW)

    guiContLot(cont_frame, "")
    guiContId(cont_frame, "")

    return cont_frame


def guiContLot(cont_frame: Frame, lot_input: str):

    for widget in cont_frame.winfo_children():
        if widget.winfo_name() == "cont_lot":
            widget.destroy()

    cont_lot_frame = Frame(cont_frame, name="cont_lot")
    cont_lot_frame.grid(row=1, column=1, sticky=EW)

    Label(cont_lot_frame, text="Lot No: ", font=("Calibri", "16")).grid(row=1, column=1)
    Label(cont_lot_frame, text=lot_input, font=("Calibri", "16")).grid(row=1, column=2)


def guiContId(cont_frame: Frame, lot_input: str):

    # Get cont and reel count from cached data
    can_cont_reels_cnt = get_cont_scan_reels_cnt(next(get_db()), lot_input)

    for widget in cont_frame.winfo_children():
        if widget.winfo_name() == "cont_id":
            widget.destroy()

    cont_id_frame = LabelFrame(
        cont_frame, name="cont_id", text="Containers", font=("Calibri", "16")
    )
    cont_id_frame.columnconfigure(0, weight=1, uniform="a")
    cont_id_frame.columnconfigure(1, weight=1, uniform="a")
    cont_id_frame.grid(row=2, column=1, sticky=NS + EW)

    for i, (cont_id, reel_cnt) in enumerate(can_cont_reels_cnt):
        Label(cont_id_frame, text=cont_id, font=("Calibri", "14")).grid(
            row=i, column=0, padx=20, pady=5, sticky=W
        )
        Label(cont_id_frame, text=reel_cnt, font=("Calibri", "14")).grid(
            row=i, column=1, padx=20, pady=5, sticky=E
        )
