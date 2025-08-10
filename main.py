import customtkinter as ctk
from ui import ChatApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = ChatApp(root)
    root.mainloop()