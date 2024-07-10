from datetime import datetime as dt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.base_class import Base


class Containers(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=False)
    date: Mapped[dt] = mapped_column(default=dt.now)
    lotNo: Mapped[str] = mapped_column(String(10))
    contid: Mapped[str]
    ReelID: Mapped[str] = mapped_column(unique=True)
