from db.initialize import db_initialize
from db.session import engine
from db.base import Base
from pages.ContainerScan import ContainerScan
from components.splash import Splash


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    db_initialize()
    root = ContainerScan()
    root = Splash(ContainerScan)
    root.mainloop()
