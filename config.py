from pathlib import Path
import sys

# config.py
APP_TITLE = "Local Chat"
WINDOW_SIZE = "800x600"
EXPERT_MODEL = "gemma3:4b-it-qat"
SMALL_MODEL = "gemma3:1b"
CUSTOM_PROMPT = (
    "You are running on weak hardware. Keep the conversation concise for swift and fast response. "
    "Answer in the language the user speaks to you."
)

def resource_path(relative_path: str) -> str:
    """
    Resolve resource paths for both dev and PyInstaller builds.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent
    return str(base_path / relative_path)
COLORS = {
    "user_bubble": "#515151",
    "bot_bubble": "#2b2b2b",
    "hover_button_color": "#CBCBCB",
    "fg_button_color": "#BABAB9",
    "fg_disabled_button_color":"#484A48",
    "fg_pressed_button_color" : "#3a7ebf",
    "hover_pressed_button_color": "#0abaff",
    "light_mode_bg" : "#FFFFFF",
    "text": "white"
}
ASSETS = {
    "send": resource_path("assets/send_arrow_icon.png"),
    "search": resource_path("assets/web_search_icon.png"),
    "expert": resource_path("assets/expert_icon.png"),
    "app_icon": resource_path("assets/app_icon.png"),
}
