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
        self.gradientStep = tk.StringVar(value=str(settings.gradient["step"]))
        self.fontsize = tk.StringVar(value=str(settings.font["size"]))
        self.curfont = tk.StringVar(value=settings.font["family"])
        self.percent = tk.StringVar(value=float(settings.output["percent"]))
        self.outputSize = tk.StringVar(value="0x0")
        self.targetWidth = tk.StringVar(value=settings.output["width"])
        self.targetHeight = tk.StringVar(value=settings.output["height"])
        self.curoutputoption = tk.StringVar(value=settings.output["type"])

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
            f'{settings.application["width"]}x{settings.application["height"]}'
        )
        return root

    def browse_image(self):
        self.curfile = fd.askopenfilename(
            parent=self.root,
            initialdir=self.curdir,
            title="select a picture",
            filetypes=(("jpg", "*.jpg"),
                       ("png", "*.png"),
                       ("All files", "*.*")))
        self.update_ascii()

    def save_ascii_file(self):
        name = os.path.basename(self.curfile)[:-4]
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
            self.curfont.get(), self.fontsize.get()))
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

    def on_gradient_step_changed(self, a, b, c):
        settings.gradient["step"] = int(self.gradientStep.get())
        self.update_ascii()

    def validate_custom_gradient(self, value):
        settings.gradient["characters"] = value
        self.update_ascii()
        return True

    def on_font_size_changed(self, a, b, c):
        val = self.fontsize.get()
        settings.font["size"] = int(val)
        self.ascii_wdiget.configure(font=(self.curfont.get(), val))

    def on_font_changed(self, a, b, c):
        settings.font["family"] = self.curfont.get()
        print(settings.font["family"])
        self.ascii_wdiget.configure(
            font=(self.curfont.get(), self.fontsize.get()))
        self.refresh_ascii_display()

    def on_output_changed(self, a, b, c):
        settings.output["type"] = self.curoutputoption.get()
        settings.output["percent"] = float(self.percent.get())
        settings.output["width"] = int(self.targetWidth.get())
        settings.output["height"] = int(self.targetHeight.get())
        self.update_ascii()

    def on_invert_gradient(self):
        gradient = settings.gradient["characters"]
        gradient = gradient[::-1]
        if self.use_custom_gradient.get():
            self.gradientEntry.set(gradient)
        settings.gradient["characters"] = gradient
        self.update_ascii()

    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.FLAT)

        # font
        fontGroup = tk.LabelFrame(toolbar, text="font", width=900, height=20)
        tk.Label(fontGroup, text="size").pack(side=tk.LEFT, padx=5)
        tk.Spinbox(fontGroup, text="font size", width=2, from_=4, to=20,
                   textvariable=self.fontsize).pack(side=tk.LEFT, padx=5, )
        fontChoices = [x for x in settings.font["options"]]
        tk.OptionMenu(fontGroup, self.curfont,
                      *fontChoices).pack(side=tk.BOTTOM, padx=5, fill=tk.X, anchor=tk.CENTER)
        self.curfont.trace('w', self.on_font_changed)
        self.fontsize.trace('w', self.on_font_size_changed)
        # gradient
        gradientGroup = tk.LabelFrame(toolbar, text="gradient")
        tk.Label(gradientGroup, text="step").pack(side=tk.LEFT, padx=10)
        tk.Spinbox(gradientGroup, width=2, from_=1,
                   to=len(settings.gradient["characters"]),
                   textvariable=self.gradientStep).pack(
                       anchor=tk.W, side=tk.LEFT)
        self.gradientStep.set(settings.gradient["step"])
        self.gradientStep.trace('w', self.on_gradient_step_changed)
        tk.Checkbutton(gradientGroup,
                       text='use custom',
                       width=10,
                       padx=5,
                       variable=self.use_custom_gradient,
                       justify=tk.RIGHT,
                       command=self.on_toggle_custom_gradient).pack(
                           anchor=tk.W, side=tk.LEFT)
        validate = self.root.register(self.validate_custom_gradient)
        entry = tk.Entry(
            gradientGroup, textvariable=self.gradientEntry, validate="key",
            validatecommand=(validate, "%P"))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10)
        self.gradientEntry.set(settings.gradient["custom"])
        settings.gradient['characters'] = settings.gradient['default']
        tk.Button(gradientGroup,
                  text="invert",
                  width=10,
                  padx=10,
                  command=self.on_invert_gradient,
                  ).pack(side=tk.LEFT, anchor=tk.W)

        # output
        outputGroup = tk.LabelFrame(toolbar, text="output", width=200)
        for val, option in settings.output["options"]:
            tk.Radiobutton(outputGroup,
                           text=val,
                           indicatoron=0,
                           width=10,
                           padx=10,
                           variable=self.curoutputoption,
                           value=val,
                           ).pack(side=tk.LEFT, anchor=tk.W)
        self.curoutputoption.trace('w', self.on_output_changed)
        tk.Label(outputGroup, text="%").pack(side=tk.LEFT, padx=10)
        tk.Spinbox(outputGroup, width=4, from_=0.05, to=2.0,
                   format="%.2f", increment=0.01,
                   textvariable=self.percent).pack(
                       anchor=tk.W, side=tk.LEFT, padx=5)
        tk.Label(outputGroup, text="width").pack(side=tk.LEFT, padx=2)
        tk.Entry(outputGroup, textvariable=self.targetWidth,
                 width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(outputGroup, text="height").pack(side=tk.LEFT, padx=2)
        tk.Entry(outputGroup, textvariable=self.targetHeight,
                 width=10).pack(side=tk.LEFT, padx=5)
        self.percent.trace('w', self.on_output_changed)
        self.targetWidth.trace('w', self.on_output_changed)
        self.targetHeight.trace('w', self.on_output_changed)

        # group pack
        gradientGroup.pack(side=tk.BOTTOM, fill=tk.X, expand=1, padx=10)
        fontGroup.pack(side=tk.LEFT, padx=10)
        outputGroup.pack(side=tk.LEFT, fill=tk.X, padx=10, expand=1)
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
