import bcrypt
from tkinter import Label

from components.messagebox import CustomMessageBox
from core.logging import logger
from db.repository.login import create_login, create_mesid, get_login, retrieve_mesid
from db.session import get_db
from pages.Register import Register
from utils.tk_windows import terminate


def passwordHasher(password: str) -> bytes:
    """Hashes the password using bcrypt."""

    pwd = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt)


def checkPassword(password: str, hash_pwd: bytes) -> bool:
    """Checks if the provided password matches the hashed password."""

    pwd = password.encode()
    return bcrypt.checkpw(pwd, hash_pwd)


def login(parent, info_text: Label) -> bool:
    """Handles user login process."""

    try:
        if check_login(parent, info_text):
            parent.res = True
            terminate(parent)
        else:
            raise Exception("Failed login. Please try again")
    except Exception as e:
        CustomMessageBox(
            parent, title="Login Failed", message=e.__str__(), mode="showerror"
        )


def register(parent, info_text: Label) -> bool:
    """Handles user registration process."""

    try:
        if Register(parent).res:
            add_credentials(parent, info_text)
        else:
            raise Exception("Failed registration. Please try again")
    except Exception as e:
        CustomMessageBox(
            parent, title="Register Failed", message=e.__str__(), mode="showerror"
        )


def check_login(parent, info_text: Label) -> bool:
    """Checks login credentials, first verifying MES ID and then user credentials."""

    text = {"text": "Please key in to continue", "bg": "red"}

    mesid_login = parent.widgets["mesid_login"].widgets

    # Check MES ID first
    mesid = mesid_login["mesid"].get()
    if mesid:
        if retrieve_mesid(next(get_db()), mesid.lower()):
            return True
        text["text"] = f"{mesid} not authorized to clear."

    # Check Login if MES ID don't exists
    user = mesid_login["user"].get()
    pwd = mesid_login["pwd"].get()
    if user and pwd:
        hash_pwd = get_login(next(get_db()), user)
        if hash_pwd and checkPassword(pwd, hash_pwd):
            return True
        text["text"] = f"Username or Password is incorrect. Please try again."

    info_text.config(text=text["text"], bg=text["bg"])
    info_text.grid(row=0, column=0, columnspan=2)

    return False


def add_credentials(parent, info_text: Label) -> None:
    """Adds new credentials to the database (MES ID or Login)."""

    text = {"text": "", "bg": "red"}

    mesid_login = parent.widgets["mesid_login"].widgets

    # Check MES ID first
    mesid = mesid_login["mesid"].get()
    if mesid:
        create_mesid(next(get_db()), mesid.lower())
        text = {"text": f"{mesid} registered!", "bg": "palegreen"}
        logger.info("%s registered as authorized member", mesid)
        return

    # Check Login if MES ID don't exists
    user = mesid_login["user"].get()
    pwd = mesid_login["pwd"].get()
    if user and pwd:
        hash_pwd = passwordHasher(pwd)
        create_login(next(get_db()), user, hash_pwd)
        text = {"text": f"{user} registered!", "bg": "palegreen"}
        logger.info("%s registered for login with password", user)

    info_text.config(text=text["text"], bg=text["bg"])
    info_text.grid(row=0, column=0, columnspan=2)
