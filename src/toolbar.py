import tkinter as tk
import src.settings as settings


class Toolbar(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self, app.root)

        toolbarRow1 = tk.Frame(app.root, bd=1, relief=tk.FLAT)
        toolbarRow2 = tk.Frame(app.root, bd=1, relief=tk.FLAT)

        # font
        fontGroup = tk.LabelFrame(
            toolbarRow1, text="font", width=900, height=20)
        tk.Label(fontGroup, text="size").pack(side=tk.LEFT, padx=5)
        tk.Spinbox(fontGroup, text="font size", width=2, from_=4, to=20,
                   textvariable=app.fontsize).pack(side=tk.LEFT, padx=5, )
        fontChoices = [x for x in settings.font["options"]]
        tk.OptionMenu(fontGroup, app.curfont,
                      *fontChoices).pack(side=tk.BOTTOM, padx=5,
                                         fill=tk.X, anchor=tk.CENTER)
        app.curfont.trace('w', app.on_font_changed)
        app.fontsize.trace('w', app.on_font_size_changed)

        # gradient
        gradientGroup = tk.LabelFrame(toolbarRow2, text="gradient")
        tk.Label(gradientGroup, text="step").pack(side=tk.LEFT, padx=10)
        tk.Spinbox(gradientGroup, width=2, from_=1,
                   to=len(settings.gradient["characters"]),
                   textvariable=app.gradientStep).pack(
                       anchor=tk.W, side=tk.LEFT)
        app.gradientStep.set(settings.gradient["step"])
        app.gradientStep.trace('w', app.on_gradient_step_changed)
        tk.Checkbutton(gradientGroup,
                       text='use custom',
                       width=8,
                       padx=5,
                       variable=app.use_custom_gradient,
                       justify=tk.RIGHT,
                       command=app.on_toggle_custom_gradient).pack(
                           anchor=tk.W, side=tk.LEFT)
        validate = app.root.register(app.validate_custom_gradient)
        entry = tk.Entry(
            gradientGroup, textvariable=app.gradientEntry, validate="key",
            validatecommand=(validate, "%P"))
        entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10)
        app.gradientEntry.set(settings.gradient["custom"])
        settings.gradient['characters'] = settings.gradient['default']
        tk.Button(gradientGroup,
                  text="invert",
                  width=8,
                  padx=10,
                  command=app.on_invert_gradient,
                  ).pack(side=tk.LEFT, anchor=tk.W)

        # output
        outputGroup = tk.LabelFrame(toolbarRow1, text="output", width=200)
        for val in settings.output["options"]:
            tk.Radiobutton(outputGroup,
                           text=val[0:-1],
                           indicatoron=0,
                           width=4,
                           padx=10,
                           variable=app.curoutputoption,
                           value=val,
                           ).pack(side=tk.LEFT, anchor=tk.W)
        app.curoutputoption.trace('w', app.on_output_changed)
        tk.Label(outputGroup, text="%").pack(side=tk.LEFT, padx=10)
        tk.Spinbox(outputGroup, width=4, from_=0.01, to=2.0,
                   format="%.2f", increment=0.01,
                   textvariable=app.percent).pack(
                       anchor=tk.W, side=tk.LEFT, padx=5)
        tk.Label(outputGroup, text="width").pack(side=tk.LEFT, padx=2)
        tk.Entry(outputGroup, textvariable=app.targetWidth,
                 width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(outputGroup, text="height").pack(side=tk.LEFT, padx=2)
        tk.Entry(outputGroup, textvariable=app.targetHeight,
                 width=10).pack(side=tk.LEFT, padx=5)
        app.percent.trace('w', app.on_output_changed)
        app.targetWidth.trace('w', app.on_output_changed)
        app.targetHeight.trace('w', app.on_output_changed)

        # adjustments
        adjustmentsGroup = tk.LabelFrame(
            toolbarRow2, text="adjustments", width=900, height=20)
        tk.Label(adjustmentsGroup, text="contrast").pack(side=tk.LEFT, padx=5)
        tk.Scale(adjustmentsGroup, from_=0.8, to=5.0, variable=app.contrast,
                 orient=tk.HORIZONTAL, width=12, resolution=0.1,
                 showvalue=0).pack(side=tk.LEFT, padx=5)
        app.contrast.trace('w', app.on_adjustments_changed)
        tk.Label(adjustmentsGroup, text="brightness").pack(
            side=tk.LEFT, padx=5)
        tk.Scale(adjustmentsGroup, from_=-255.0, to=255.0,
                 variable=app.brightness,
                 orient=tk.HORIZONTAL, width=12, resolution=0.1,
                 showvalue=0).pack(side=tk.LEFT, padx=5)
        app.contrast.trace('w', app.on_adjustments_changed)
        app.brightness.trace('w', app.on_adjustments_changed)

        # group pack
        fontGroup.pack(side=tk.LEFT, padx=10)
        outputGroup.pack(side=tk.LEFT, fill=tk.X, padx=10, expand=1)
        gradientGroup.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=10)
        adjustmentsGroup.pack(side=tk.LEFT, fill=tk.X, padx=10)
        toolbarRow1.pack(side=tk.TOP, fill=tk.X)
        toolbarRow2.pack(side=tk.TOP, fill=tk.X)
