import os
import cv2
import numpy as np
import math
from sizing import getWidth, getHeight


def rgb_to_character(value, gradient):
    return gradient[int((value / 255) * (len(gradient) - 1))]


def grey(path, settings):
    if not os.path.isfile:
        print("provided path isn't an image")
        return None
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)


def resize(img, settings):
    try:
        dsize = (settings.output["width"], settings.output["height"])
        if dsize[0] <= 0 or dsize[1] <= 0:
            return ""

        height = int(settings.output["height"])
        width = int(settings.output["width"])
        dsize = (width, height)

        resized = cv2.resize(img, dsize=dsize, interpolation=cv2.INTER_AREA)
        return resized
    except ValueError:
        print("img is not the right format")


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
