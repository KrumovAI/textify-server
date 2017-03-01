import cv2
import textify.utils.image_processing as image_processing
from textify.utils.rectangle import Rectangle
from PIL import Image


def get_contours(thresh):
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_contours(im, contours, width, height):
    for rect in contours:
        x, y, w, h = cv2.boundingRect(rect)

        if w <= 0.9 * width and h <= 0.9 * height:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 0), -1)


def draw_contours_outline(im, contours, width, height):
    for rect in contours:
        x, y, w, h = cv2.boundingRect(rect)

        if w <= 0.9 * width and h <= 0.9 * height:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)


def process_img(filename):
    img = Image.open(filename)
    # img = image_processing.expand(img)
    image = image_processing.resize(img, 35)
    img = image_processing.paste(image, False)
    img.save(filename)


def filter_rects(rects, area):
    to_remove = list()
    for rect in rects:
        rect_area = rect.width * rect.height
        if rect_area <= 0.0001 * area or rect_area >= 0.9 * area:
            to_remove.append(rect)

    for rect in to_remove:
        rects.remove(rect)

    return rects


def contours_ro_rects(contours):
    rects = list()

    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        rects.append(Rectangle(x, y, w, h, cont))

    return rects


def sort_rects(rects):
    rects.sort(key=lambda r: r.y, reverse=False)
    rows = list()

    while len(rects) > 0:
        rect = rects[0]
        rects.remove(rect)
        to_remove = list()
        row = [rect]

        for other in rects:
            if abs(rect.y - other.y) < 0.6 * rect.height:
                row.append(other)
                to_remove.append(other)
            else:
                break

        for rem in to_remove:
            rects.remove(rem)

        row.sort(key=lambda r: r.x, reverse=False)
        rows.append(row)

    sorted_rects = sum(rows, [])
    return sorted_rects


def get_words(letters):
    words = list()
    word = list()
    avg_width = sum(r.width for r in letters) / len(letters)
    avg_height = sum(r.height for r in letters) / len(letters)

    for i in range(1, len(letters)):
        rect1 = letters[i - 1]
        rect2 = letters[i]
        dif_hor = float(abs(rect2.x - (rect1.x + rect1.width)))
        dif_ver = float(abs(rect2.height - rect1.height))

        if dif_hor <= 0.7 * avg_width and dif_ver <= round(0.3 * avg_height):
            if len(word) == 0:
                word.append(rect1)

            word.append(rect2)

            if i == len(letters) - 1:
                words.append(word)
        else:
            if rect1 not in word:
                word.append(rect1)
                words.append(word)
                word = []

            if rect2 not in word and i == len(letters) - 1:
                word.append(rect2)

            if len(word) != 0:
                words.append(word)

            word = []

    return words
