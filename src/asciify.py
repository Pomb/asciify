import os
import cv2


def rgb_to_character(value, gradient):
    return gradient[int((value / 255) * (len(gradient) - 1))]


def convert_image_to_characters(path, settings):
    if not path:
        return ""
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    resized = cv2.resize(img, dsize=(
                         int(img.shape[1] * settings.output["sizePercent"]),
                         int(img.shape[0] * settings.output["sizePercent"])),
                         interpolation=cv2.INTER_NEAREST)

    ascii_characters = ""
    for x in range(resized.shape[0]):
        for y in range(resized.shape[1]):
            ascii_characters += rgb_to_character(
                resized[x, y], settings.gradient["characters"])
        ascii_characters += '\n'
    return ascii_characters
    # cv2.imshow('image', resized)
    # cv2.waitKey(0)  # waits until a key is pressed
    # cv2.destroyAllWindows()  # destroys the window showing image
    # save_image(resized, os.path.basename(path)[:-4])
    # save_text_ascii(ascii_image, os.path.basename(path)[:-4])
