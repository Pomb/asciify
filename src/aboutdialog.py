import tkinter as tk
from src.hyperlinkmanager import HyperlinkManager
import webbrowser


class AboutDialog():
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.geometry('350x150')
        self.top.transient(parent)
        self.top.grab_set()
        self.top.title("About")
        self.top.bind("<Escape>", lambda e: self.top.destroy)

        tk.Label(self.top, text="ASCIIFY",
                 justify=tk.CENTER, font=("Lucida Sans Typewriter", 26)).pack(
            side=tk.TOP, padx=20, pady=10)
        self.text = tk.Text(self.top, height=2, bg="#f0f0f0", relief=tk.FLAT)
        self.text.tag_configure("center", justify='center')

        self.hyperlink = HyperlinkManager(self.text)
        self.text.insert(tk.INSERT, "website",
                         self.hyperlink.add(self.open_docs))

        self.text.tag_add("center", "1.0", "end")
        self.text.pack()

        tk.Label(self.top, text="build XXXX", justify=tk.CENTER).pack()

    def open_docs(self):
        print('open docs')
        webbrowser.open_new("https://pomb.github.io/asciify/")
