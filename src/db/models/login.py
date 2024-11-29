from datetime import datetime as dt
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Login(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=False)
    date: Mapped[dt] = mapped_column(default=dt.now)
    user: Mapped[int] = mapped_column(String)
    password: Mapped[int] = mapped_column(String)


class MESID(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    date: Mapped[dt] = mapped_column(default=dt.now)
    mesid: Mapped[str] = mapped_column(String(8), unique=True)
