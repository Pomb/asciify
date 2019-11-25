import tkinter as tk


class MenuBar():
    def __init__(self, app):
        menubar = tk.Menu(app.root)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=app.browse_image)
        fileMenu.add_command(label="Save", command=app.save_ascii_file)

        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=app.root.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=app.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        app.root.config(menu=menubar)
