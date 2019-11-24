import os
import cv2


def rgb_to_character(value, gradient):
    return gradient[int((value / 255) * (len(gradient) - 1))]


def convert_image_to_characters(path, settings, callback):
    if not path:
        return ""
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.convertScaleAbs(
        img, alpha=settings.adjustments["contrast"],
        beta=settings.adjustments["brightness"])
    dsize = img.shape
    if "scale" in settings.output["type"]:
        dsize = (int(img.shape[1] * settings.output["percent"]),
                 int(img.shape[1] * settings.output["percent"]))
    else:
        dsize = (settings.output["width"], settings.output["height"])

    resized = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_NEAREST)

    ascii_characters = ""
    for x in range(resized.shape[0]):
        for y in range(resized.shape[1]):
            ascii_characters += rgb_to_character(
                resized[x, y], settings.gradient["characters"])
        ascii_characters += '\n'

    callback(resized)
    return ascii_characters
