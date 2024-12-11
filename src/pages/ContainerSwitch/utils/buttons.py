from db.repository.casing import update_reel_data
from db.session import get_db
from utils.error_handler import update_label_exceptions


def update_db(parent) -> None:
    """Handles the update of reel data in the database and updates UI labels."""

    info_widget = parent.widgets["switch_info"].widgets["info"]

    try:
        container_reels = parent.widgets["containers_reels"]
        old_cont_id = container_reels.widgets["old_container"].widgets["contid"].get()
        new_cont_id = container_reels.widgets["new_container"].widgets["contid"].get()

        if len(old_cont_id) != 10 or len(new_cont_id) != 10:
            raise ValueError("Please scan Container ID to transfer")
        if len(container_reels.cache["Old"]) or not len(container_reels.cache["New"]):
            raise ValueError("Please scan all reels to transfer")

        for reel_data in container_reels.cache["New"]:
            reel_dict = reel_data.__dict__
            reel_id = reel_dict.pop("ReelID")
            update_reel_data(next(get_db()), reel_id, reel_dict)

        text = f"Successfully updated from {old_cont_id} to {new_cont_id}."
        update_label_exceptions(info_widget, text, "palegreen")

        parent.res = True

    except Exception as e:
        update_label_exceptions(info_widget, e.__str__(), "tomato")
