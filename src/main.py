from db.base import Base
from db.session import engine
from db.initialize import mesid_initialize
from pages.ContainerScan import ContainerScan
from components.splash import Splash


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    mesid_initialize()
    root = Splash(ContainerScan)
    root.mainloop()
