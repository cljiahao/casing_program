from tkinter import CENTER, E, EW, NS, RAISED, W
from tkinter import (
    Button,
    Entry,
    Frame,
    Label,
    LabelFrame,
    messagebox,
    Toplevel,
)

from core.logging import logger
from db.repository.casing import (
    get_scan_reel_data,
    update_reel_data,
)
from db.session import get_db
from utils.casing import check_state, clearValue


class ContainerSwitch(Toplevel):
    def __init__(self, lot_no: str):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.initialize(lot_no)
        self.win_config()
        self.widgets()
        self.grab_set()
        self.mainloop()

    def exit(self):
        self.destroy()
        self.quit()

    def initialize(self, lot_no: str):
        self.lot_no = lot_no
        self.res = False
        self.text = "Scan old and new containers below to transfer."
        self.old_reel_data = []
        self.new_reel_data = []

    def cb_entry(self, input: str, name: str):
        key = name.split(".")[-1]
        match key:
            case "old":
                if len(input) == 10:
                    self.check_and_update(key, input, self.old_reel_data)
            case "new":
                if len(input) == 10:
                    self.check_and_update(key, input, self.new_reel_data)
            case "reel":
                if len(input) == 15:
                    old_cont_input = self.cont_dict["old"]["entry"].get()
                    new_cont_input = self.cont_dict["new"]["entry"].get()
                    old_exists = check_state(self.lot_no, old_cont_input, True)
                    new_exists = check_state(self.lot_no, new_cont_input)

                    text_input = ""
                    if not old_exists and not new_exists:
                        text_input = "Container [old and new]"
                    elif not new_exists:
                        text_input = "Container [new]"
                    elif not old_exists:
                        text_input = "Container [old]"
                    else:
                        reel_exists = False
                        for i, reel_data in enumerate(self.old_reel_data):
                            if reel_data.ReelID == input:
                                reel_exists = True
                                reel_data.contid = new_cont_input
                                self.new_reel_data.append(reel_data)
                                del self.old_reel_data[i]
                                self.refresh_reel_frame("old", self.old_reel_data)
                                self.refresh_reel_frame("new", self.new_reel_data)
                        if not reel_exists:
                            text_input = f"ReelID: {input}"

                    if text_input:
                        text = f"Please check and confirm {text_input}."
                        bg = "tomato"
                        logger.info(text)
                    else:
                        text = self.text
                        bg = "lightgrey"
                    self.info.config(text=text, bg=bg)

                    clearValue(self.cont_dict["reel"])

        return True

    def check_and_update(self, key: str, cont_input: str, reel_data: list):
        text = self.text
        bg = "lightgrey"
        lot_cont_exists = check_state(self.lot_no, cont_input, key == "old")
        if lot_cont_exists:
            reel_data.clear()
            reel_data.extend(
                get_scan_reel_data(next(get_db()), self.lot_no, cont_input)
            )
            self.cont_dict[key]["frame"].config(text=cont_input)
            if key == "old":
                self.cont_dict["new"]["entry"].focus()
            else:
                self.cont_dict["reel"].focus()
        else:
            bg = "tomato"
            grammar = "does not" if key == "old" else ""
            text = f"Container [{key}]: {cont_input} {grammar} exists in database."
            reel_data = []
            clearValue(self.cont_dict[key]["entry"])
            logger.info(text)

        self.info.config(text=text, bg=bg)
        self.cont_dict[key]["frame"].config(text=cont_input)
        self.refresh_reel_frame(key, reel_data)

    def refresh_reel_frame(self, cont_type: str, reel_data: list):

        for widget in self.cont_dict[cont_type]["frame"].winfo_children():
            widget.destroy()

        for i, reel in enumerate(reel_data):
            Label(self.cont_dict[cont_type]["frame"], text=reel.ReelID).grid(
                row=i // 2, column=i % 2
            )

    def update_db(self):

        bg = "palegreen"
        if len(self.old_reel_data) or not len(self.new_reel_data):
            text = f"Please scan all reels to transfer."
            bg = "tomato"
            logger.info(text)
        else:
            try:
                for reel_data in self.new_reel_data:
                    reel_id = reel_data.ReelID
                    reel_dict = reel_data.__dict__
                    del reel_dict["ReelID"]
                    update_reel_data(next(get_db()), reel_id, reel_dict)
            except Exception as e:
                logger.error("Unable to update reel data in database", exc_info=True)
                messagebox.showerror(e.__str__())

            text = f"Update to new container completed. Please continue."

        self.info.config(text=text, bg=bg)

    def win_config(self):
        self.title("Switch Containers")
        screen_size = {
            "h_screen": self.winfo_screenheight(),
            "w_screen": self.winfo_screenwidth(),
        }
        self.config(bg="lightgrey", bd=20)
        self.geometry(
            f"{int(screen_size['w_screen']/2)}x{int(screen_size['h_screen']*3/4)}+{int(screen_size['w_screen']/4)}+{int(screen_size['h_screen']/25)}"
        )
        self.reg_entry = (self.register(self.cb_entry), "%P", "%W")
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

    def widgets(self):

        self.info = Label(
            self,
            text=self.text,
            bg="lightgrey",
            font=("Calibri", "16"),
            relief=RAISED,
        )
        self.info.grid(row=0, column=1, columnspan=2, pady=7, ipady=10, sticky=NS + EW)

        self.cont_dict = {"old": {}, "new": {}}
        for i, cont_type in enumerate(self.cont_dict):

            cont_entry_frame = Frame(self, bg="lightgrey")
            cont_entry_frame.columnconfigure(0, weight=1)
            cont_entry_frame.columnconfigure(1, weight=1)
            cont_entry_frame.grid(row=1, column=i + 1, padx=10, pady=7, sticky=NS + EW)

            Label(
                cont_entry_frame,
                text=f"Container [{cont_type}]",
                bg="lightgrey",
                font=("Calibri", "12"),
            ).grid(row=i, column=i * 2 + 1, padx=(0, 5), sticky=EW)

            self.cont_dict[cont_type]["entry"] = Entry(
                cont_entry_frame,
                name=cont_type.lower(),
                font=("Calibri", "12"),
                justify=CENTER,
                validate="key",
                validatecommand=self.reg_entry,
            )
            self.cont_dict[cont_type]["entry"].grid(row=i, column=i * 2 + 2)

            self.cont_dict[cont_type]["frame"] = LabelFrame(
                self,
                text=" ",
                font=("Calibri", "14"),
            )
            self.cont_dict[cont_type]["frame"].columnconfigure(0, weight=1)
            self.cont_dict[cont_type]["frame"].columnconfigure(1, weight=1)
            self.cont_dict[cont_type]["frame"].grid(
                row=2, column=i + 1, padx=10, pady=7, sticky=NS + EW
            )

        reel_entry_frame = Frame(self, bg="lightgrey")
        reel_entry_frame.columnconfigure(1, weight=1)
        reel_entry_frame.grid(
            row=3, column=1, columnspan=2, padx=10, pady=7, sticky=NS + EW
        )

        Label(
            reel_entry_frame,
            text=f"Reel ID",
            bg="lightgrey",
            font=("Calibri", "12"),
        ).grid(row=0, column=0, padx=5, sticky=W)

        self.cont_dict["reel"] = Entry(
            reel_entry_frame,
            name="reel",
            font=("Calibri", "12"),
            width=50,
            justify=CENTER,
            validate="key",
            validatecommand=self.reg_entry,
        )
        self.cont_dict["reel"].grid(row=0, column=1, ipady=2, sticky=E)

        button_frame = Frame(self, bg="lightgrey")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.grid(row=4, column=1, columnspan=2, padx=5, pady=(7, 0), sticky=EW)

        Button(
            button_frame,
            text="Cancel",
            bg="firebrick2",
            fg="whitesmoke",
            font=("Calibri", "12", "bold"),
            command=lambda: self.exit(),
        ).grid(row=0, column=0, ipady=2)
        Button(
            button_frame,
            text="Confirm",
            bg="palegreen",
            font=("Calibri", "12"),
            command=lambda: self.update_db(),
        ).grid(row=0, column=1, ipady=2)
