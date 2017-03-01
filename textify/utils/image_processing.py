import cv2
import PIL
from PIL import Image
import math
import os


def expand(img, loops=1):
    pix = img.load()
    w, h = img.size

    for l in range(loops):
        tuples = []

        for i in range(1, w - 1):
            for j in range(1, h - 1):
                if pix[i, j] == 255:
                    if pix[i - 1, j] == 0 or pix[i - 1, j - 1] == 0 or pix[i - 1, j + 1] == 0 or pix[
                        i, j - 1] == 0 or pix[i, j + 1] == 0 or pix[i + 1, j - 1] == 0 or pix[i + 1, j] == 0 or pix[
                                i + 1, j + 1] == 0:
                        tuples.append((i, j))

        for pixel_tuple in tuples:
            pix[pixel_tuple] = 0

    return img


def threshold(im, is_grayscale):
    if not is_grayscale:
        # BGR to grayscale
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    border = 100

    ret, thresh = cv2.threshold(im, border, 255, cv2.THRESH_BINARY)
    return thresh


def resize(img, baseheight):
    w, h = img.size
    if w > h:
        baseheight = int(baseheight * 0.75)
    new_width = int(math.ceil((baseheight / h) * w))

    return img.resize((new_width, baseheight), PIL.Image.ANTIALIAS)


def paste(img, use_mask, x_offset=0, y_offset=0):
    width, height = img.size
    background_path = os.path.join(os.getcwd(), os.path.join('textify', 'img'))
    background = Image.open(os.path.join(background_path, "sample.png")).convert('L')
    bg_w, bg_h = background.size
    offset = (int((bg_w - width) / 2) + x_offset, int((bg_h - height) / 2) + y_offset)

    if use_mask:
        background.paste(img, offset, img)
    else:
        background.paste(img, offset)

    background = background.convert('L')
    return background
