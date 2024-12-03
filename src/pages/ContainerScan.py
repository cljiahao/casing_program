from tkinter import BOTH
from tkinter import Tk, Frame

from apis.api_pmss import api_get_lot_data
from core.logging import logger
from components.buttons import guiButtons
from components.containers import guiCont, guiContId, guiContLot
from components.wos import guiWOS
from pages.ContainerSwitch import ContainerSwitch
from pages.Login import Login
from utils.casing import (
    clearValue,
    contId,
    endLot,
    lotNo,
    reelId,
    reelValidation,
)


class ContainerScan(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.initialize()
        self.win_config()
        self.widgets()

    def initialize(self):
        self.cache = {"optcode": False, "lot": False, "contid": False}
        self.reel_per_box = 0
        self.reel_id = ""

    def cb_entry(self, input: str, name: str):
        """Call backs for Entry"""
        key_name = name.split(".")[-1]
        try:
            match key_name:
                case "optcode":
                    self.cache["optcode"] = False
                    if len(input) == 7:
                        self.cache["optcode"] = True
                        self.wos_entry["lotNo"].focus()

                case "lotno":
                    self.cache["lot"] = False
                    if len(input) == 10:
                        self.reel_per_box, self.reel_id = lotNo(
                            self.wos_entry, input, self.cache
                        )
                        guiContLot(self.cont_frame, input)
                        guiContId(self.cont_frame, input)

                case "contid":
                    self.cache["contid"] = False
                    if len(input) == 10:
                        lot_no = self.wos_entry["lotNo"].get()
                        contId(
                            self.wos_entry, lot_no, input, self.reel_per_box, self.cache
                        )
                        guiContId(self.cont_frame, lot_no)

                case "reelid":
                    if len(input) == 15:
                        lot_no = self.wos_entry["lotNo"].get()
                        reelId(
                            self.wos_entry,
                            input,
                            self.reel_per_box,
                            self.reel_id,
                            self.cache,
                        )
                        guiContId(self.cont_frame, lot_no)

        except Exception as e:
            logger.error(e, exc_info=True)
            while True:
                if Login(e.__str__()).res:
                    break
            key = [k for k in self.wos_entry.keys() if k.lower() == key_name][0]
            clearValue(self.wos_entry[key])

        return True

    def reset(self):
        for widget in self.frame.winfo_children():
            if widget.winfo_name() in ["wos", "container"]:
                widget.destroy()

        self.wos_entry = guiWOS(self.frame, self.reg_entry)
        self.cont_frame = guiCont(self.frame)
        self.cache = {"optcode": False, "lot": False, "contid": False}

    def switch(self):
        try:
            if Login("Login to Start Container Switch.").res:
                lot_no = self.wos_entry["lotNo"].get()

                # API call to server if lot exists
                json = api_get_lot_data(lot_no)
                if json["code"] != "0":
                    raise LookupError(json["message"])

                if ContainerSwitch(lot_no).res:
                    guiContId(self.cont_frame, lot_no)
                    clearValue(self.wos_entry["contid"])
        except Exception as e:
            logger.error(e, exc_info=True)
            while True:
                if Login(e.__str__()).res:
                    break

    def refresh(self):
        try:
            lot_no = self.wos_entry["lotNo"].get()

            # API call to server if lot exists
            json = api_get_lot_data(lot_no)
            if json["code"] != "0":
                raise LookupError(json["message"])

            lot_data = json["data"]
            reel_ids = lot_data.pop("ReelID")

            # TODO: Question: Refresh need a pop up to show that it was refreshed?
            validation = reelValidation(lot_no, reel_ids)
            if validation:
                raise ValueError(f"Reels not fully scanned. Missing {validation}.")
        except Exception as e:
            logger.error(e, exc_info=True)
            while True:
                if Login(e.__str__()).res:
                    break

        guiContId(self.cont_frame, lot_no)

    def end_lot(self):

        res = False
        lot_no = self.wos_entry["lotNo"].get()
        opt_code = self.wos_entry["OptCode"].get()
        try:
            res = endLot(lot_no, opt_code)
        except Exception as e:
            logger.error(e, exc_info=True)
            while True:
                if Login(e.__str__()).res:
                    break
        if res:
            self.reset()

    def win_config(self):
        self.title("Casing Scan")
        self.state("zoomed")
        self.frame = Frame(self)
        self.frame.rowconfigure(0, weight=15, uniform="a")
        self.frame.rowconfigure(1, weight=2, uniform="a")
        for i in range(5):
            weight = 1 if i % 2 == 0 else 10
            self.frame.columnconfigure(i, weight=weight, uniform="a")
        self.frame.columnconfigure(1, weight=17, uniform="a")
        self.frame.pack(fill=BOTH, expand=True, pady=30)
        self.reg_entry = (self.register(self.cb_entry), "%P", "%W")
        self.button_info = {
            "switch": {
                "text": "Switch",
                "onClick": self.switch,
                "bg": "royalblue1",
                "fg": "whitesmoke",
                "font": ("Calibri", "14", "bold"),
            },
            "refresh": {
                "text": "Refresh",
                "onClick": self.refresh,
                "bg": "palegreen",
                "fg": "black",
                "font": ("Calibri", "14"),
            },
            "lotend": {
                "text": "Lot End",
                "onClick": self.end_lot,
                "bg": "firebrick2",
                "fg": "whitesmoke",
                "font": ("Calibri", "14", "bold"),
            },
        }

    def widgets(self):

        self.wos_entry = guiWOS(self.frame, self.reg_entry)

        self.cont_frame = guiCont(self.frame)

        guiButtons(self.frame, self.button_info)
