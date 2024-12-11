from utils.tk_windows import terminate


def ask_yes_no(root, button_text: str):
    """Set the response based on the button text and terminate the window."""

    root.res = button_text.lower() == "yes"
    terminate(root)


def show_(root, *args):
    """Terminate the window."""

    terminate(root)
