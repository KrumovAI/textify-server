from textify.models import Drawing
from django.core.files.images import ImageFile
from textify.utils.symbols import symbols
import os
import uuid


def fill_drawings(user):
    drawings = user.drawing_set.all()
    basepath = os.getcwd()

    for i in range(26):
        labeled = drawings.filter(label_index=i)
        if len(labeled) == 0:
            path = basepath + '\\textify\handwritten\\' + str(i)
            files = os.listdir(path)

            for file in files:
                if file != 'Thumbs.db' and file != 'data':
                    img = ImageFile(open(path + '\\' + file, 'rb'))
                    db_pic = Drawing(user_id=user.id, name=file, label_index=i, label=symbols[i])
                    db_pic.image.save(basepath + '/user_files/drawings/' + str(uuid.uuid4()) + '.png', img, True)
