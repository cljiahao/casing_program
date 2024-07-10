from tkinter import EW, RAISED
from tkinter import Entry, Label, Toplevel

from core.logging import logger
from db.repository.login import retrieve_mesid
from db.session import get_db
from utils.casing import clearValue


class Register(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.initialize()
        self.win_config()
        self.widgets()
        self.grab_set()
        self.mainloop()

    def exit(self):
        self.destroy()
        self.quit()

    def initialize(self):
        self.res = False

    def cb_entry(self, input, name):
        """Call backs for Entry"""
        key_name = name.split(".")[-1]
        match key_name:
            case "mesid":
                if len(input) == 8:
                    self.res = retrieve_mesid(next(get_db()), input.lower())
                    logger.info("%s scanned to authorize", input)
                    if self.res:
                        self.exit()
                    else:
                        clearValue(self.mesid_entry)

        return True

    def win_config(self):
        self.title("Register")
        screen_size = {
            "h_screen": self.winfo_screenheight(),
            "w_screen": self.winfo_screenwidth(),
        }
        self.config(bg="#DDD", bd=20)
        self.geometry(
            f"{int(screen_size['w_screen']/3)}x{int(screen_size['h_screen']/5)}+{int(screen_size['w_screen']*1/3)}+{int(screen_size['h_screen']/35)}"
        )
        self.reg_entry = (self.register(self.cb_entry), "%P", "%W")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(3, weight=10)
        self.columnconfigure(4, weight=1)

    def widgets(self):

        Label(
            self,
            text="Please scan authorized personnel's MES ID",
            bg="#FFF",
            fg="#CF352E",
            font=("Calibri", 12, "bold"),
            relief=RAISED,
        ).grid(row=0, column=1, rowspan=2, columnspan=3, pady=10, ipady=7, sticky=EW)

        # MES ID
        Label(self, text="MES ID:", bg="#DDD", font=("Calibri", 12)).grid(
            row=2, column=1
        )
        self.mesid_entry = Entry(
            self,
            name="mesid",
            validate="key",
            validatecommand=self.reg_entry,
        )
        self.mesid_entry.grid(row=2, column=2, columnspan=2, ipady=3, ipadx=20, pady=3)

        self.mesid_entry.focus()
