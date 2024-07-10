from tkinter import *

from db.initialize import db_initialize
from db.session import engine
from db.base_class import Base
from pages.ContainerScan import ContainerScan

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    db_initialize()
    root = ContainerScan()
    root.mainloop()
