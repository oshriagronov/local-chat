import customtkinter as ctk
from tkinter import Canvas, Frame, PhotoImage
import tkinter.font as tkfont
from PIL import Image, ImageTk
import threading
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
        self.request_in_flight = False
        self.pending_bot_label = None
        # Build the user interface
        self.build_ui() 

    def build_ui(self):
        # Configure grid layout to allow resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.chat_horizontal_padding = 8
        self.message_min_width = 72
        self.message_max_width_ratio = 0.82
        self.message_min_height = 18
        self.message_vertical_spacing = 2
        self.message_text_pad_x = 8
        self.message_text_pad_y = 1
        self.message_bottom_buffer = 6
        self.message_font = ctk.CTkFont(size=13)
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
        self.frame_window = self.chat_canvas.create_window(
            (self.chat_horizontal_padding, 0),
            window=self.messages_frame,
            anchor="nw"
        )
        # Adjust the width of the messages frame to match the canvas width on resize
        self.chat_canvas.bind(
            "<Configure>",
            lambda e: self.chat_canvas.itemconfig(
                self.frame_window,  # the window ID we store
                width=max(e.width - (self.chat_horizontal_padding * 2), 1)
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
        self.web_search_button = self.create_button(self.input_frame, ASSETS["search"], self.toggle_web_search,col = 2, state="disabled", fg_color=COLORS["fg_disabled_button_color"])
        self.expert_button = self.create_button(self.input_frame, ASSETS["expert"], self.toggle_expert, col = 1)

    def create_button(self,parent, img_path, command, col, fg_color=COLORS["fg_button_color"],state="normal"):
        """
        Create a button with an icon image, custom colors, and bind it to a command.
        """
        img = Image.open(img_path).resize((40,40))
        btn = ctk.CTkButton(parent,state=state, text=None, fg_color=fg_color, hover_color=COLORS["hover_button_color"], corner_radius=30 ,width=0, command=command,image=ctk.CTkImage(img))
        btn.grid(row=0,column=col , pady= 5, padx=5)
        return btn
    
    def send_message(self, event=None):
        """
        Called when the user presses Enter or clicks the send button.
        Sends the user's message to the logic handler and displays both user and bot messages.
        """
        if self.request_in_flight:
            return "break"

        user_msg = self.entry.get().strip()
        if not user_msg:
            return "break"

        self.add_message(user_msg, "user")
        self.entry.delete(0, ctk.END)
        self.pending_bot_label = self.add_message("Thinking", "bot")
        self.request_in_flight = True
        self._set_send_button_state(enabled=False)
        worker = threading.Thread(
            target=self._process_message_async,
            args=(user_msg,),
            daemon=True
        )
        worker.start()
        return "break"

    def _process_message_async(self, message: str):
        try:
            response = self.logic.process_message(message)
        except Exception as exc:
            response = f"Error: {exc}"
        self.root.after(0, lambda: self._on_model_response(response))

    def _on_model_response(self, response: str):
        if self.pending_bot_label and self.pending_bot_label.winfo_exists():
            self._set_message_text(self.pending_bot_label, response)
        else:
            self.add_message(response, "bot")
        self.pending_bot_label = None
        self.request_in_flight = False
        self._set_send_button_state(enabled=True)

    def _set_send_button_state(self, enabled: bool):
        if enabled:
            self.send_button.configure(
                state="normal",
                fg_color=COLORS["fg_button_color"],
                hover_color=COLORS["hover_button_color"]
            )
            return

        self.send_button.configure(
            state="disabled",
            fg_color=COLORS["fg_disabled_button_color"],
            hover_color=COLORS["fg_disabled_button_color"]
        )

    def _calculate_message_width(self, widget, text):
        """
        Calculate bubble width from content, capped by the available canvas width.
        """
        self.root.update_idletasks()
        canvas_width = self.chat_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = self.root.winfo_width()

        max_width = max(
            int(canvas_width * self.message_max_width_ratio),
            self.message_min_width
        )
        font = tkfont.Font(font=widget._textbox.cget("font"))
        lines = text.splitlines() if text else [""]
        # Measure with a trailing space to account for textbox internal padding.
        longest_line_width = max(font.measure(f"{line} ") for line in lines)
        # Keep extra headroom so short status texts do not wrap awkwardly.
        content_width = longest_line_width + (self.message_text_pad_x * 2) + 22
        return min(max(content_width, self.message_min_width), max_width)

    def _resize_message_widget(self, widget):
        """
        Resize a message widget height to fit wrapped content while keeping it read-only.
        """
        self.root.update_idletasks()

        font = tkfont.Font(font=widget._textbox.cget("font"))
        line_height = font.metrics("linespace")
        display_lines = 1
        try:
            tk_result = widget._textbox.tk.call(
                widget._textbox._w,
                "count",
                "-displaylines",
                "1.0",
                "end-1c"
            )
            display_lines = int(tk_result) if tk_result else 1
        except Exception:
            display_lines = 1
        content_height = max(display_lines, 1) * line_height

        final_height = (
            content_height
            + (self.message_text_pad_y * 2)
            + self.message_bottom_buffer
        )
        widget.configure(height=max(final_height, self.message_min_height))
        self.root.update_idletasks()

        # Safety pass: if Tk still reports hidden content, grow a few lines.
        for _ in range(3):
            _first, last = widget._textbox.yview()
            if last >= 0.999:
                break
            final_height += line_height
            widget.configure(height=final_height)
            self.root.update_idletasks()

        widget._textbox.yview_moveto(0)

    def _set_message_text(self, widget, text):
        """
        Replace message content and keep the widget read-only for selection/copy.
        """
        widget.configure(state="normal")
        widget.configure(width=self._calculate_message_width(widget, text))
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget._textbox.tag_add("align", "1.0", "end")
        self._resize_message_widget(widget)
        widget.configure(state="disabled")

    def add_message(self, text, sender):
        """
        Add a message bubble to the chat area.
        Adjusts color, text alignment, and padding depending on sender (user or bot).
        """
        bubble_color = COLORS["user_bubble"] if sender == "user" else COLORS["bot_bubble"]
        text_color = "white"
        message_widget = ctk.CTkTextbox(
            self.messages_frame,
            fg_color=bubble_color,
            text_color=text_color,
            corner_radius=10,
            wrap="word",
            width=self.message_min_width,
            height=self.message_min_height,
            border_width=0,
            activate_scrollbars=False,
            font=self.message_font
        )
        message_widget._textbox.configure(
            relief="flat",
            borderwidth=0,
            padx=self.message_text_pad_x,
            pady=self.message_text_pad_y,
            insertwidth=0,
            spacing1=0,
            spacing2=0,
            spacing3=0
        )
        # Prevent per-bubble scrolling; the outer chat canvas handles scrolling.
        message_widget._textbox.bind("<MouseWheel>", lambda _e: "break")
        message_widget._textbox.bind("<Shift-MouseWheel>", lambda _e: "break")
        message_widget._textbox.bind("<Button-4>", lambda _e: "break")
        message_widget._textbox.bind("<Button-5>", lambda _e: "break")
        # Keep both user and bot text left-aligned for cleaner wrapped lines.
        message_widget._textbox.tag_configure("align", justify="left")
        message_widget.pack(
            anchor="e" if sender=="user" else "w",
            pady=self.message_vertical_spacing,
            padx=(0, 5)
        )
        # Size after packing so wrapping/line metrics use real geometry.
        self._set_message_text(message_widget, text)
        # Auto-scroll to the bottom with a slight delay to ensure update
        self.root.after(50, lambda: self.chat_canvas.yview_moveto(1.0))
        return message_widget

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
