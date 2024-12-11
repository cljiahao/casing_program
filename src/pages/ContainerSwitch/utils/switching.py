from tkinter import Label

from core.constants import font_size


def refresh_reel_frame(root, mode: str) -> None:
    """Refreshes the reel frame by clearing existing widgets and displaying new reel data."""

    container_reel_ids = root.widgets[f"{mode}_container"].widgets["reelids"]
    # Destroy existing widgets in the reel frame
    for widget in container_reel_ids.winfo_children():
        widget.destroy()

    # Create new labels for each reel ID
    for i, reel in enumerate(root.cache[mode.capitalize()]):
        Label(container_reel_ids, text=reel.ReelID, font=font_size["M"]).grid(
            row=i // 2, column=i % 2, pady=2
        )
