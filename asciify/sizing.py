import math


def calculateAspectRatioFit(width, height, maxWidth=2048, maxHeight=2048):
    ratio = min(maxWidth / width, maxHeight / height)
    return (int(width*ratio), int(height*ratio))


def getHeight(length, ratio):
    height = ((length)/(math.sqrt((math.pow(ratio, 2)+1))))
    return round(height)


def getWidth(length, ratio):
    width = ((length)/(math.sqrt((1)/(math.pow(ratio, 2)+1))))
    return round(width)
