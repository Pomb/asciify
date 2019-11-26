import os
import cv2
import numpy as np


def rgb_to_character(value, gradient):
    return gradient[int((value / 255) * (len(gradient) - 1))]


def resize(path, settings):
    if not path:
        return None
    dsize = (settings.output["width"], settings.output["height"])
    if dsize[0] <= 0 or dsize[1] <= 0:
        return ""

    # black and white
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if "scale" in settings.output["type"]:
        dsize = (int(img.shape[1] * settings.output["percent"]),
                 int(img.shape[1] * settings.output["percent"]))

    resized = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)
    return resized


def convert_image_to_characters(img, settings):
    if img is None:
        return ""
    # contrast
    img = cv2.convertScaleAbs(
        img, alpha=settings.adjustments["contrast"],
        beta=settings.adjustments["brightness"])
    # sharpen
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img = cv2.filter2D(img, -2, kernel)

    ascii_characters = ""
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            ascii_characters += rgb_to_character(
                img[x, y], settings.gradient["characters"])
        ascii_characters += '\n'

    return ascii_characters
