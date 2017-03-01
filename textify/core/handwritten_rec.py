import numpy
import uuid
from textify.utils.contours_processing import *
import textify.utils.image_processing as image_processing
from textify.utils.symbols import *
from PIL import Image
import os


def textify(pil_img, classifier):
    filename = str(uuid.uuid4()) + '.png'
    w, h = pil_img.size
    pil_img = image_processing.resize(pil_img, 2000)
    pil_img.save(filename)
    im = cv2.imread(filename)
    rectangles = contours_ro_rects(extract_contours(im))
    rectangles = filter_rects(rectangles, w * h)
    rectangles = sort_rects(rectangles)
    result = get_result(rectangles, filename, classifier)
    os.remove(filename)
    return result


def extract_contours(im):
    thresh_filename = str(uuid.uuid4()) + 'thresh.png'
    temp_filename = str(uuid.uuid4()) + 'temp.png'
    thresh = image_processing.threshold(im, False)
    cv2.imwrite(thresh_filename, thresh)
    cv2.imwrite(temp_filename, thresh)
    pil_img = Image.open(temp_filename)
    w, h = pil_img.size
    pil_img.close()
    contours = get_contours(thresh)
    img = cv2.imread(temp_filename)
    draw_contours(img, contours, w, h)
    thresh2 = image_processing.threshold(img, False)
    get_contours(thresh2)
    cv2.imwrite(temp_filename, img)
    img2 = cv2.imread(temp_filename)
    thresh3 = image_processing.threshold(img2, False)
    contours3 = get_contours(thresh3)
    # img3 = cv2.imread('thresh.png')
    # draw_contours_outline(img3, contours3, w, h)
    # cv2.imwrite('cont_test.png', img3)
    cv2.imwrite(temp_filename, img2)
    os.remove(thresh_filename)
    os.remove(temp_filename)
    return contours3


def get_result(rectangles, filename, classifier):
    thresh = image_processing.threshold(cv2.imread(filename), False)
    thresh_filename = str(uuid.uuid4()) + 'thresh.png'
    cv2.imwrite(thresh_filename, thresh)
    img = Image.open(thresh_filename)
    counter = 0
    filtered_rects = []
    results = []

    for rect in rectangles:
        temp_name = str(uuid.uuid4()) + 'temp-crop.png'
        crop = img.crop((rect.x, rect.y, rect.x + rect.width, rect.y + rect.height))
        crop.convert('RGBA')
        crop.save(temp_name)
        process_img(temp_name)
        processed = image_processing.threshold(cv2.imread(temp_name), False)

        symbol = get_symbol(processed, classifier)
        # cv2.imwrite('tests/test-' + str(counter) + '-' + symbol + '.png', processed)
        filtered_rects.append(rect)
        results.append(symbol)
        counter += 1
        os.remove(temp_name)

    words = get_words(filtered_rects)
    os.remove(thresh_filename)
    return process_result(words, results)


def process_result(words, results):
    letter_counter = 0
    text = ""

    for word in words:
        word_text = ""

        for i in range(len(word)):
            word_text += results[letter_counter]
            letter_counter += 1

        text += word_text
        text += " "

    return text


def get_symbol(img, classifier):
    array = numpy.reshape(img, (len([img]), -1))
    index = classifier.predict(array)[0]
    return symbols[index]

# print(textify(r'C:\Users\Emil\Pictures\demo2.jpg'))
