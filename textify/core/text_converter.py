from PIL import Image
import pytesseract
import cv2
import os
import uuid

class TextConverter:
    @staticmethod
    def convert(filename):
        initial = cv2.imread(filename)
        im_gray = cv2.cvtColor(initial, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(im_gray, 200, 255, cv2.THRESH_BINARY_INV)
        temp_filename = os.path.join(os.path.join(os.getcwd(), 'user_files'), str(uuid.uuid4()) + 'temp.jpg')
        cv2.imwrite(temp_filename, thresh)

        img = Image.open(temp_filename)
        text = pytesseract.image_to_string(img)
        text = os.linesep.join([s for s in text.splitlines() if s])
        os.remove(temp_filename)
        return text
