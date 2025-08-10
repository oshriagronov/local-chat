import customtkinter as ctk
from tkinter import Canvas, Frame
from PIL import Image
from logic import ChatLogic
from config import COLORS, ASSETS, APP_TITLE, WINDOW_SIZE
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.logic = ChatLogic()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        ctk.set_appearance_mode("system")
        self.build_ui()
    def build_ui(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.chat_canvas = Canvas(self.root, bg=None if ctk.get_appearance_mode() == "Dark" else COLORS["light_mode_bg"], highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self.root,orientation="vertical", command=self.chat_canvas.yview)
        self.messages_frame = Frame(self.chat_canvas, bg=None if ctk.get_appearance_mode() == "Dark" else COLORS["light_mode_bg"])
        self.messages_frame.bind(
        "<Configure>",
        lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        self.frame_window = self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        self.chat_canvas.bind(
            "<Configure>",
            lambda e: self.chat_canvas.itemconfig(
                self.frame_window,  # the window ID we store
                width=e.width
            )
        )
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.chat_canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ask anything", corner_radius=10)
        self.entry.grid(row=0, column=0, sticky="ew", padx=5)
        self.entry.bind("<Return>", self.send_message)
        self.send_button = self.create_button(self.input_frame, ASSETS["send"], self.send_message,col = 3)
        self.web_search_button = self.create_button(self.input_frame, ASSETS["search"], self.toggle_web_search,col = 2, state="disabled")
        self.expert_button = self.create_button(self.input_frame, ASSETS["expert"], self.toggle_expert, col = 1)
    def create_button(self,parent, img_path, command, col, state="normal"):
        img = Image.open(img_path).resize((40,40))
        btn = ctk.CTkButton(parent,state=state, text=None, fg_color=COLORS["fg_button_color"], hover_color=COLORS["hover_button_color"], corner_radius=30 ,width=0, command=command,image=ctk.CTkImage(img))
        btn.grid(row=0,column=col , pady= 5, padx=5)
        return btn
    def send_message(self, event=None):
        user_msg = self.entry.get().strip()
        if not user_msg:
            return
        self.add_message(user_msg, "user")
        self.entry.delete(0, ctk.END)
        self.add_message(self.logic.process_message(user_msg), "bot")
    def add_message(self, text, sender):
        bubble_color = COLORS["user_bubble"] if sender == "user" else COLORS["bot_bubble"]
        text_color = "white"
        justify = "right" if sender == "user" else "left"
        label = ctk.CTkLabel(
            self.messages_frame,
            text=text,
            fg_color=bubble_color,
            text_color=text_color,
            corner_radius=10,
            wraplength=500,
            anchor="w" if sender == "bot" else "e",
            justify=justify,
            pady=5,
            padx=10
        )
        label.pack(anchor="e" if sender=="user" else "w", pady=5, padx=(0, 5) if sender == "user" else (0,5))
        self.root.after(50, lambda: self.chat_canvas.yview_moveto(1.0))

    def toggle_web_search(self):
        self.logic.toggle_web_search()
        self.web_search_button.configure(hover_color=COLORS["hover_pressed_button_color"] if self.logic.web_search_mode == True else COLORS["hover_button_color"],
            fg_color=COLORS["fg_pressed_button_color"] if self.logic.web_search_mode else COLORS["fg_button_color"]
        )

    def toggle_expert(self):
        self.logic.toggle_expert()
        self.expert_button.configure(hover_color=COLORS["hover_pressed_button_color"] if self.logic.expert_mode == True else COLORS["hover_button_color"],
            fg_color=COLORS["fg_pressed_button_color"] if self.logic.expert_mode else COLORS["fg_button_color"]
        )
        self.web_search_button.configure(
            state="normal" if self.logic.expert_mode else "disabled",
            fg_color=COLORS["fg_button_color"] if self.logic.expert_mode else COLORS["fg_disabled_button_color"]
        )