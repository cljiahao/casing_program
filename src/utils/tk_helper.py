from tkinter import E, W
from tkinter import Label

from apis.api_cm import api_set_empty_cont
from components.messagebox import CustomMessageBox
from core.constants import wos_labels, font_size
from db.repository.casing import get_cont_scan_reels_cnt, get_scan_reels_cnt
from db.session import get_db
from utils.api_utils import check_cont_empty


def reset_container(root, cont_id: str) -> None:
    """Resets the container if not empty by confirming with the user."""

    if not check_cont_empty(cont_id):
        if not CustomMessageBox(
            root,
            title="Reset Container if not empty",
            message="Is Container Empty?",
            mode="askyesno",
        ).res:
            raise ValueError(f"Wrong container ID: {cont_id} scanned")
        api_set_empty_cont(cont_id)


def refresh_container_widget(root, lot_no: str) -> None:
    """Refreshes the container widget by destroying the old one and creating a new instance."""

    # Get cont and reel count from cached data
    can_cont_reels_cnt = get_cont_scan_reels_cnt(next(get_db()), lot_no)

    cont_info_cont_id = root.widgets["cont_info"].widgets["cont_id"]
    # Destroy existing widgets in the reel frame
    for widget in cont_info_cont_id.winfo_children():
        widget.destroy()

    # Create new labels for each Container ID and count
    for i, (cont_id, reel_cnt) in enumerate(can_cont_reels_cnt):
        Label(cont_info_cont_id, text=cont_id, font=font_size["XL"]).grid(
            row=i, column=0, padx=20, pady=5, sticky=W
        )
        Label(cont_info_cont_id, text=reel_cnt, font=font_size["XL"]).grid(
            row=i, column=1, padx=20, pady=5, sticky=E
        )


def refresh_reel_count_widget(
    root, lot_no: str, lot_data: dict[str, str | list[str]]
) -> None:
    """Updates the reel count in the UI based on scanned reels in the database."""

    # Get the count of scanned reels from the database
    reel_count = get_scan_reels_cnt(next(get_db()), lot_no)

    label_type_wos = [label["key"] for label in wos_labels if label["type"] == "label"]
    for key, value in lot_data.items():
        if key in root.cache.keys() and key in label_type_wos:
            if key == "noOfReel":
                value = f"{reel_count} / {value}"
            root.cache[key].set(value)
