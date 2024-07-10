from tkinter import EW, LEFT, NS, RAISED
from tkinter import Button, Entry, Frame, Label, messagebox, Toplevel

from pages.Register import Register
from utils.login import addCredentials, checkLogin


# Convert Login to use database instead
class Login(Toplevel):
    def __init__(self, error: str):
        Toplevel.__init__(self)
        self.protocol("WM_DELETE_WINDOW", self.exit)
        self.initialize()
        self.win_config()
        self.widgets(error)
        self.grab_set()
        self.mainloop()

    def exit(self):
        self.destroy()
        self.quit()

    def initialize(self):
        self.res = False

    def check_login(self, entry_dict: dict, info_text: Label):
        try:
            if checkLogin(entry_dict, info_text):
                self.res = True
                self.exit()
        except Exception as e:
            messagebox.showerror(e.__str__())

    def register(self, entry_dict: dict, info_text: Label):
        try:
            if Register().res:
                addCredentials(entry_dict, info_text)
        except Exception as e:
            messagebox.showerror(e.__str__())

    def win_config(self):
        self.title("Login")
        screen_size = {
            "h_screen": self.winfo_screenheight(),
            "w_screen": self.winfo_screenwidth(),
        }
        self.config(bg="#A4C0D6", bd=20)
        self.geometry(
            f"{int(screen_size['w_screen']/3)}x{int(screen_size['h_screen']*3/5)}+{int(screen_size['w_screen']/3)}+{int(screen_size['h_screen']/35)}"
        )
        self.rowconfigure(0, weight=1)
        self.rowconfigure(7, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(3, weight=10)
        self.columnconfigure(4, weight=1)

    def widgets(self, error):

        Label(
            self,
            text=error,
            wraplength=300,
            bg="#FFF",
            fg="#CF352E",
            font=("Calibri", 12, "bold"),
            relief=RAISED,
            justify=LEFT,
        ).grid(row=0, column=1, rowspan=2, columnspan=3, pady=10, ipady=7, sticky=EW)

        entry_dict = {"mesid": {}, "user": {}, "pwd": {}}
        name = ["MES ID", "Username", "Password"]

        info_text = Label(self, font=("Calibri", 12))

        for i, key in enumerate(entry_dict.keys()):
            row = int(-0.5 * i**2 + 2.5 * i + 2)
            Label(self, text=name[i], bg="#A4C0D6", font=("Calibri", 12)).grid(
                row=row, column=1
            )
            entry_dict[key]["entry"] = Entry(self)
            entry_dict[key]["entry"].grid(
                row=row, column=2, columnspan=2, ipady=3, ipadx=20, pady=3
            )

        entry_dict["pwd"]["entry"].config(show="*")

        Label(self, text="OR", bg="#A4C0D6", font=("Calibri", 12, "bold")).grid(
            row=3, column=1, columnspan=3, pady=15
        )

        but_frame = Frame(self, bg="#A4C0D6")
        but_frame.columnconfigure(0, weight=1)
        but_frame.columnconfigure(2, weight=1)
        but_frame.columnconfigure(4, weight=1)
        but_frame.grid(row=8, column=0, columnspan=4, sticky=NS + EW)

        Button(
            but_frame,
            text="Register",
            font=("Calibri", 12),
            command=lambda: self.register(entry_dict, info_text),
        ).grid(row=8, column=1, pady=5, ipadx=5)

        Button(
            but_frame,
            text="Login",
            font=("Calibri", 12),
            command=lambda: self.check_login(entry_dict, info_text),
        ).grid(row=8, column=3, pady=5, ipadx=5)

        entry_dict["mesid"]["entry"].focus()
