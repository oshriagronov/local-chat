import customtkinter as ctk
from ui import ChatApp

if __name__ == "__main__":
    """
    Attention! the "expert" model gemma3:4b require 16GB of Ram and a decent GPU(I will say 2GB Vram at the very lest) for good experience.
    if you not meet the recommendation above, please use the regular model(don't use web search and the "expert" mode).
    The "expert" model is a lot more accurate and "smarter" but consume a lot of resources, use them as you see fit.

    The best use cases for the models are:
    1. Summarization
    2. Proofread
    3. Simple text tasks
    4. Answer to questions about pdf files(maybe in future update)
    """
    root = ctk.CTk()
    app = ChatApp(root)
    root.mainloop()