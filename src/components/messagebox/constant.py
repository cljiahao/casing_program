from components.messagebox.utils.buttons import show_, ask_yes_no


messagebox_info = {
    "showinfo": {
        "bg_color": "#E8E7E5",
        "logo_name": "info-icon.png",
        "button_texts": ["Ok"],
        "command": show_,
    },
    "showerror": {
        "bg_color": "#FFCCCC",
        "logo_name": "error-icon.png",
        "button_texts": ["Ok"],
        "command": show_,
    },
    "showwarning": {
        "bg_color": "#E8E7E5",
        "logo_name": "warning-icon.png",
        "button_texts": ["Confirm"],
        "command": show_,
    },
    "askyesno": {
        "bg_color": "#D2D2CF",
        "logo_name": "question-icon.png",
        "button_texts": ["Yes", "No"],
        "command": ask_yes_no,
    },
}
