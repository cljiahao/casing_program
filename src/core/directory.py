import os


class Directory:
    base_path = os.path.dirname(os.path.dirname(__file__))

    log_path = os.path.join(base_path, "log")
    data_path = os.path.join(base_path, "data")


directory = Directory()
