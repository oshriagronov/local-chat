# config.py
APP_TITLE = "Local Chat"
WINDOW_SIZE = "800x600"
EXPERT_MODEL = "gemma3:4b-it-qat"
SMALL_MODEL = "gemma3:1b"
CUSTOM_PROMPT = "You are running on weak hardware. Keep the conversation concise for swift and fast response. Answer in the language the user speaks to you."
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
    "send": "./assets/send_arrow_icon.png",
    "search": "./assets/web_search_icon.png",
    "expert": "./assets/expert_icon.png"
}