import customtkinter as ctk
from tkinter import Canvas, Frame, PhotoImage
from PIL import Image, ImageTk
from logic import ChatLogic
from config import COLORS, ASSETS, APP_TITLE, WINDOW_SIZE
class ChatApp:
    def __init__(self, root):
        self.root = root
        # Initialize chat logic handler
        self.logic = ChatLogic()
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        # setting the icon for the app
        self.root.iconphoto(True, ImageTk.PhotoImage(Image.open(ASSETS["app_icon"])))
        # Automatically use system light/dark mode
        ctk.set_appearance_mode("system")
        # Build the user interface
        self.build_ui() 

    def build_ui(self):
        # Configure grid layout to allow resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        # Create a canvas for displaying chat messages with dynamic background color
        self.chat_canvas = Canvas(self.root, bg=None if ctk.get_appearance_mode() == "Dark" else COLORS["light_mode_bg"], highlightthickness=0)
        # Vertical scrollbar for the chat canvas
        self.scrollbar = ctk.CTkScrollbar(self.root,orientation="vertical", command=self.chat_canvas.yview)
        # Frame to hold chat message widgets inside the canvas
        self.messages_frame = Frame(self.chat_canvas, bg=None if ctk.get_appearance_mode() == "Dark" else COLORS["light_mode_bg"])
        # Update the scroll region when the messages frame size changes
        self.messages_frame.bind(
        "<Configure>",
        lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all"))
        )
        # Add the messages frame to the canvas as a window item
        self.frame_window = self.chat_canvas.create_window((0, 0), window=self.messages_frame, anchor="nw")
        # Adjust the width of the messages frame to match the canvas width on resize
        self.chat_canvas.bind(
            "<Configure>",
            lambda e: self.chat_canvas.itemconfig(
                self.frame_window,  # the window ID we store
                width=e.width
            )
        )
        # Connect scrollbar to canvas scrolling
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)
        # Position the canvas and scrollbar in the grid
        self.chat_canvas.grid(row=1, column=0, sticky="nsew")
        self.scrollbar.grid(row=1, column=1, sticky="ns")
        # Frame for input field and buttons at the bottom
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=5)
        self.input_frame.grid_columnconfigure(0, weight=1)
        # Text entry widget for user input with placeholder text
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ask anything", corner_radius=10)
        self.entry.grid(row=0, column=0, sticky="ew", padx=5)
        # Bind Enter key to sending the message
        self.entry.bind("<Return>", self.send_message)
        # Create buttons: send message, toggle web search, toggle expert mode
        self.send_button = self.create_button(self.input_frame, ASSETS["send"], self.send_message,col = 3)
        self.web_search_button = self.create_button(self.input_frame, ASSETS["search"], self.toggle_web_search,col = 2, state="disabled")
        self.expert_button = self.create_button(self.input_frame, ASSETS["expert"], self.toggle_expert, col = 1)

    def create_button(self,parent, img_path, command, col, state="normal"):
        """
        Create a button with an icon image, custom colors, and bind it to a command.
        """
        img = Image.open(img_path).resize((40,40))
        btn = ctk.CTkButton(parent,state=state, text=None, fg_color=COLORS["fg_button_color"], hover_color=COLORS["hover_button_color"], corner_radius=30 ,width=0, command=command,image=ctk.CTkImage(img))
        btn.grid(row=0,column=col , pady= 5, padx=5)
        return btn
    
    def send_message(self, event=None):
        """
        Called when the user presses Enter or clicks the send button.
        Sends the user's message to the logic handler and displays both user and bot messages.
        """
        user_msg = self.entry.get().strip()
        if not user_msg:
            return
        self.add_message(user_msg, "user")
        self.entry.delete(0, ctk.END)
        self.add_message(self.logic.process_message(user_msg), "bot")

    def add_message(self, text, sender):
        """
        Add a message bubble to the chat area.
        Adjusts color, text alignment, and padding depending on sender (user or bot).
        """
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
        # Auto-scroll to the bottom with a slight delay to ensure update
        self.root.after(50, lambda: self.chat_canvas.yview_moveto(1.0))

    def toggle_web_search(self):
        """
        Toggle the web search mode on/off.
        Update the button appearance accordingly.
        Only available if expert mode is active.
        """
        self.logic.toggle_web_search()
        self.web_search_button.configure(hover_color=COLORS["hover_pressed_button_color"] if self.logic.web_search_mode == True else COLORS["hover_button_color"],
            fg_color=COLORS["fg_pressed_button_color"] if self.logic.web_search_mode else COLORS["fg_button_color"]
        )

    def toggle_expert(self):
        """
        Toggle the expert mode on/off.
        Update the expert button and enable/disable the web search button accordingly.
        """
        self.logic.toggle_expert()
        self.expert_button.configure(hover_color=COLORS["hover_pressed_button_color"] if self.logic.expert_mode == True else COLORS["hover_button_color"],
            fg_color=COLORS["fg_pressed_button_color"] if self.logic.expert_mode else COLORS["fg_button_color"]
        )
        self.web_search_button.configure(
            state="normal" if self.logic.expert_mode else "disabled",
            fg_color=COLORS["fg_button_color"] if self.logic.expert_mode else COLORS["fg_disabled_button_color"]
        )