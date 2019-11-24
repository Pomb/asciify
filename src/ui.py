import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox
import os
from src.asciify import convert_image_to_characters
from PIL import Image, ImageTk
import src.settings as settings
import time
import json


class ascii_application():
    def __init__(self):
        self.root = self._create_root_app()
        self.curdir = os.getcwd()
        self.curfile = ""
        self.ascii_image = ""
        self.gradientEntry = tk.StringVar()
        self.use_custom_gradient = tk.BooleanVar(value=False)
        self.gradientStep = tk.StringVar()

        # application elements
        self.ascii_wdiget = self.create_ascii_zone()
        self.menubar = MenuBar(self)
        self.toolbar_widget = self.create_toolbar()

        # construct the loop the window
        self.root.mainloop()

    def _create_root_app(self):
        root = tk.Tk()
        root.geometry(
            f'{settings.application["windowWidth"]}x{settings.application["windowHeight"]}')
        return root

    def browse_image(self):
        self.curfile = fd.askopenfilename(parent=self.root, initialdir=self.curdir, title="select a picture", filetypes=(
            ("jpg", "*.jpg"), ("png", "*.png"), ("All files", "*.*")))
        self.update_ascii()

    def save_ascii_file(self):
        name = os.path.basename(self.curfile)[:-4]
        print(name)
        filename = os.path.join(self.curdir, 'images/', f'{name}_ascii.txt')
        print('save', filename)
        with open(filename, 'w') as outputfile:
            outputfile.writelines(self.ascii_image)

    def refresh_ascii_display(self):
        self.ascii_wdiget.delete(1.0, tk.END)
        self.ascii_wdiget.insert(tk.END, self.ascii_image)

    def create_ascii_zone(self):
        # ascii text zone
        text1 = tk.Text(self.root, font=(
            settings.font["family"], settings.font["fontSize"]))
        text1.pack(expand=1, fill='both', padx=10, pady=10, side=tk.BOTTOM)
        return text1

    def update_ascii(self):
        print(settings.gradient["characters"])
        if not self.curfile:
            print('error no file currently avaialble to asciify')
            return
        if len(settings.gradient['characters']) == 0:
            print('error not enough characters to make asciified image')
            return
        self.ascii_image = convert_image_to_characters(
            self.curfile, settings)
        self.refresh_ascii_display()

    def show_about(self):
        messagebox.showinfo("About", "documentation not yet downloaded")

    def on_toggle_custom_gradient(self):
        if self.use_custom_gradient.get():
            settings.gradient["characters"] = self.gradientEntry.get()
        else:
            settings.gradient["characters"] = settings.gradient["default"]
        self.update_ascii()

    def on_gradient_step_changed(self, value):
        self.gradientStep.set(value)
        settings.gradient["step"] = value
        self.update_ascii()

    def validate_custom_gradient(self, value):
        settings.gradient["characters"] = value
        self.update_ascii()
        return True

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)

        tk.Label(toolbar, text="step").pack(side=tk.LEFT)
        tk.Scale(toolbar,
                 from_=1,
                 to=len(settings.gradient["characters"]),
                 orient=tk.HORIZONTAL,
                 width=5,
                 showvalue=0,
                 command=self.on_gradient_step_changed).pack(anchor=tk.W, side=tk.LEFT)
        self.gradientStep.set(settings.gradient["step"])
        tk.Label(toolbar, width=5, textvariable=self.gradientStep).pack(
            side=tk.LEFT)

        tk.Checkbutton(toolbar,
                       text='use custom gradient',
                       width=20,
                       padx=5,
                       variable=self.use_custom_gradient,
                       justify=tk.RIGHT,
                       command=self.on_toggle_custom_gradient).pack(anchor=tk.W, side=tk.LEFT)

        validate = self.root.register(self.validate_custom_gradient)
        entry = tk.Entry(
            toolbar, textvariable=self.gradientEntry, validate="key",
            validatecommand=(validate, "%P"))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1)

        tk.Button(toolbar, text="update",  width=15,
                  command=self.update_ascii).pack(side=tk.RIGHT, padx=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        return toolbar


class MenuBar():
    def __init__(self, app):
        menubar = tk.Menu(app.root)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=app.browse_image)
        fileMenu.add_command(label="Save", command=app.save_ascii_file)

        fileMenu.add_separator()
        fileMenu.add_command(label="Quit", command=app.root.quit)
        menubar.add_cascade(label="file", menu=fileMenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=app.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        app.root.config(menu=menubar)
