import base64
from textify.models import User
from textify.utils.fill import *
from textify.core.data_collectors import *


def get_drawings(user_id, label):
    try:
        user = User.objects.get(id=user_id)
        drawings = user.drawing_set.filter(label_index=label)
        result = []

        for drawing in drawings:
            file = drawing.image.path
            with open(file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                result.append(encoded_string.decode('utf-8'))

        return result
    except User.DoesNotExist:
        result = []
        path = os.getcwd() + '/textify/handwritten/' + str(label)

        for file in os.listdir(path):
            if file != 'data' and file != 'Thumbs.db':
                with open(path + '/' + file, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    result.append(encoded_string.decode('utf-8'))

        return result


def upload_drawings(user_id, name, label_index, file):
    basepath = os.getcwd()

    try:
        user = User.objects.get(pk=user_id)
        try:
            db_drawing = user.drawing_set.get(name=name, label_index=label_index)
            db_drawing.image.save(basepath + '/user_files/drawings/' + str(uuid.uuid4()) + '.png', file, True)
        except Drawing.DoesNotExist:
            db_drawing = user.drawing_set.create(name=name, label_index=label_index,
                                                 label=symbols[int(float(label_index))])
            db_drawing.image.save(basepath + '/user_files/drawings/' + str(uuid.uuid4()) + '.png', file, True)

        return True
    except User.DoesNotExist:
        return False
