import bcrypt
from tkinter import Label

from core.logging import logger
from db.repository.login import create_login, create_mesid, get_login, retrieve_mesid
from db.session import get_db


def passwordHasher(password: str) -> bytes:
    pwd = password.encode()
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(pwd, salt)
    return hash_pwd


def checkPassword(password: str, hash_pwd: bytes) -> bool:
    pwd = password.encode()
    return bcrypt.checkpw(pwd, hash_pwd)


def checkLogin(entry_dict: dict, info_text: Label) -> bool:

    text = {"text": "Please key in to continue.", "bg": "red"}

    # Check MES ID first
    mesid_login = entry_dict["mesid"]["entry"].get()
    if mesid_login:
        if retrieve_mesid(next(get_db()), mesid_login.lower()):
            return True
        text["text"] = f"{mesid_login} not authorized to clear."

    # Check Login if MES ID don't exists
    user = entry_dict["user"]["entry"].get()
    pwd = entry_dict["pwd"]["entry"].get()
    if user and pwd:
        hash_pwd = get_login(next(get_db()), user)
        if hash_pwd:
            if checkPassword(pwd, hash_pwd):
                return True
        text["text"] = f"Username or Password is incorrect. Please try again."

    info_text.config(text=text["text"], bg=text["bg"])
    info_text.grid(row=6, column=0, columnspan=4)

    return False


def addCredentials(entry_dict: dict, info_text: Label) -> None:

    text = {"text": "", "bg": "red"}

    # Check MES ID first
    mesid_login = entry_dict["mesid"]["entry"].get()
    if mesid_login:
        create_mesid(next(get_db()), mesid_login.lower())
        text = {"text": f"{mesid_login} registered!", "bg": "palegreen"}
        logger.info("%s registered as authorized member", mesid_login)
        return

    # Check Login if MES ID don't exists
    user = entry_dict["user"]["entry"].get()
    pwd = entry_dict["pwd"]["entry"].get()
    if user and pwd:
        hash_pwd = passwordHasher(pwd)
        create_login(next(get_db()), user, hash_pwd)
        text = {"text": f"{user} registered!", "bg": "palegreen"}
        logger.info("%s registered for login with password", user)

    info_text.config(text=text["text"], bg=text["bg"])
    info_text.grid(row=6, column=0, columnspan=4)
