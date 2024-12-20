from pathlib import Path
from PIL import Image, ImageTk
from tkinter import END, Entry


def window_size(root) -> dict[str, int | float]:
    """Returns the screen dimensions and aspect ratio of the root window."""

    win_size = {
        "w_screen": root.winfo_screenwidth(),
        "h_screen": root.winfo_screenheight(),
        "aspect": root.winfo_screenwidth() / root.winfo_screenheight(),
    }
    return win_size


def image_resize(
    path: Path, win_size: dict[str, int | float], multiplier: float
) -> ImageTk.PhotoImage:
    """Resizes an image based on window size and multiplier, returning a PhotoImage object."""

    image = Image.open(path)
    image_aspect = image.width / image.height
    logo_height = int(win_size["height"] * multiplier)
    logo_width = int(image_aspect * logo_height)
    resize = image.resize((logo_width, logo_height))
    return ImageTk.PhotoImage(resize)


def loop_till_approve(tk_window, root, *args) -> None:
    """Loops until the given Tk window returns a truthy result for approval."""

    while True:
        if tk_window(root, *args).res:
            break


def terminate(root) -> None:
    """Terminates the Tkinter window."""

    root.destroy()
    root.quit()


def clear_value(widget: any) -> None:
    """Clears the value of a widget (e.g., an entry field) after idle time."""

    widget.after_idle(lambda: delete_entry(widget))
    widget.focus()


def delete_entry(entry_value: Entry) -> None:
    """Deletes the content of an Entry widget."""

    entry_value.delete(0, END)
    entry_value.configure(validate="key")
