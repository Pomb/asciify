import tkinter as tk
import tkinter.filedialog as fd
from tkinter import messagebox
import cv2
import os
from img_to_char import convert_image_to_characters
from img_to_char import resize
import settings as settings
import time
import json
from menubar import MenuBar
from toolbar import Toolbar
from about_dialog import AboutDialog


class AsciifyGUI():
    def __init__(self):
        self.root = self._create_root_app()
        self.curdir = os.getcwd()
        self.curfile = ""
        self.curimg = None
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
        self.contrast = tk.StringVar(value=settings.adjustments["contrast"])
        self.brightness = tk.StringVar(
            value=settings.adjustments["brightness"])

        # application elements
        self.ascii_wdiget = self.create_ascii_zone()
        self.menubar = MenuBar(self)
        self.toolbar_widget = Toolbar(self)

    def run(self):
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
        self.update_current_working_img()
        self.update_ascii()

    def save_ascii_file(self):
        name = os.path.basename(self.curfile)[:-4]
        filename = fd.asksaveasfilename(
            initialfile=f"{name}_ascii",
            defaultextension=".txt",
            initialdir=self.curdir,
            filetypes=(("txt", "*.txt"),
                       ("All files", "*.*")))
        print('save', filename)
        if filename is not None:
            with open(filename, 'w') as outputfile:
                outputfile.writelines(self.ascii_image)

    def refresh_ascii_display(self):
        self.ascii_wdiget.delete(1.0, tk.END)
        self.ascii_wdiget.insert(tk.END, self.ascii_image)

    def create_ascii_zone(self):
        text1 = tk.Text(self.root, font=(
            self.curfont.get(), self.fontsize.get()))
        text1.pack(expand=1, fill='both', padx=10, pady=10, side=tk.BOTTOM)
        return text1

    def update_ascii(self):
        if self.curimg is None:
            print('error no file currently avaialble to asciify')
            return
        if len(settings.gradient['characters']) == 0:
            print('error not enough characters to make asciified image')
            return
        self.ascii_image = convert_image_to_characters(self.curimg, settings)
        self.refresh_ascii_display()

    def show_about(self):
        d = AboutDialog(self.root)
        self.root.wait_window(d.top)

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
        self.ascii_wdiget.configure(
            font=(self.curfont.get(), self.fontsize.get()))
        self.refresh_ascii_display()

    def update_current_working_img(self):
        try:
            self.curimg = resize(self.curfile, settings)
            self.outputSize.set(
                f'{self.curimg.shape[0]}x{self.curimg.shape[1]}')
        except AttributeError:
            print("no current img to update")

    def on_outputsize_changed(self, a, b, c):
        if self.targetWidth.get() == "":
            self.targetWidth.set(0)
        if self.targetHeight.get() == "":
            self.targetHeight.set(0)

        settings.output["type"] = self.curoutputoption.get()
        settings.output["percent"] = float(self.percent.get())
        settings.output["width"] = int(self.targetWidth.get())
        settings.output["height"] = int(self.targetHeight.get())

        if self.curfile is None:
            return

        self.update_current_working_img()
        self.update_ascii()

    def on_invert_gradient(self):
        gradient = settings.gradient["characters"]
        gradient = gradient[::-1]
        if self.use_custom_gradient.get():
            self.gradientEntry.set(gradient)
        settings.gradient["characters"] = gradient
        self.update_ascii()

    def on_adjustments_changed(self, a, b, c):
        settings.adjustments["contrast"] = float(self.contrast.get())
        settings.adjustments["brightness"] = float(self.brightness.get())
        self.update_ascii()
