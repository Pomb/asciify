import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox
import os
from src.asciify import convert_image_to_characters
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
        self.fontsize = tk.StringVar(value=str(settings.font["size"]))
        self.outputSize = tk.StringVar(value="0x0")

        # application elements
        self.ascii_wdiget = self.create_ascii_zone()
        self.menubar = MenuBar(self)
        self.toolbar_widget = self.create_toolbar()

        # construct the loop the window
        self.root.mainloop()

    def _create_root_app(self):
        root = tk.Tk()
        root.title("Asciify")
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
            settings.font["family"], self.fontsize.get()))
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
            self.curfile, settings, self.on_ascii_image_updated)
        self.refresh_ascii_display()

    def on_ascii_image_updated(self, resized_img):
        print(resized_img.shape)
        self.outputSize.set(f'{resized_img.shape[0]}x{resized_img.shape[1]}')

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

    def on_font_size_changed(self, a, b, c):
        val = self.fontsize.get()
        settings.font["size"] = int(val)
        self.ascii_wdiget.configure(font=(settings.font["family"], val))

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.FLAT)
        fontGroup = tk.LabelFrame(toolbar, text="settings")

        tk.Label(fontGroup, text="font size").pack(side=tk.LEFT, padx=10)
        tk.Spinbox(fontGroup, text="font size", width=2, from_=4, to=20,
                   textvariable=self.fontsize).pack(side=tk.LEFT, padx=10)
        self.fontsize.trace('w', self.on_font_size_changed)

        gradientGroup = tk.LabelFrame(toolbar, text="gradient")
        tk.Label(gradientGroup, text="step").pack(side=tk.LEFT, padx=10)
        tk.Scale(gradientGroup,
                 from_=1,
                 to=len(settings.gradient["characters"]),
                 orient=tk.HORIZONTAL,
                 width=5,
                 showvalue=0,
                 command=self.on_gradient_step_changed).pack(anchor=tk.W, side=tk.LEFT)
        self.gradientStep.set(settings.gradient["step"])
        tk.Label(gradientGroup, width=5, textvariable=self.gradientStep).pack(
            side=tk.LEFT)

        tk.Checkbutton(gradientGroup,
                       text='use custom gradient',
                       width=20,
                       padx=10,
                       variable=self.use_custom_gradient,
                       justify=tk.RIGHT,
                       command=self.on_toggle_custom_gradient).pack(anchor=tk.W, side=tk.LEFT)

        validate = self.root.register(self.validate_custom_gradient)
        entry = tk.Entry(
            gradientGroup, textvariable=self.gradientEntry, validate="key",
            validatecommand=(validate, "%P"))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10)

        self.gradientEntry.set(settings.gradient["custom"])
        settings.gradient['characters'] = settings.gradient['default']

        outputGroup = tk.LabelFrame(toolbar, text="output")

        tk.Label(outputGroup, textvariable=self.outputSize, width=10).pack(
            side=tk.LEFT, padx=10)
        # tk.Button(toolbar, text="update",  width=15,
        #           command=self.update_ascii).pack(side=tk.RIGHT, padx=10)
        fontGroup.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)
        gradientGroup.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10)
        outputGroup.pack(side=tk.RIGHT, fill=tk.X, padx=10)
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
        menubar.add_cascade(label="File", menu=fileMenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=app.show_about)
        menubar.add_cascade(label="Help", menu=helpmenu)

        app.root.config(menu=menubar)
