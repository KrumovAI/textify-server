import os
import shutil
import textify.utils.data_generation as data_generation
from PIL import Image


def get_data(user, user_folder):
    path = os.path.join(os.getcwd(), 'user_files')
    path = os.path.join(path, user_folder)

    if not os.path.isdir(path):
        os.makedirs(path)

    path = os.path.join(path, 'handwritten')

    if not os.path.isdir(path):
        os.makedirs(path)

    for i in range(26):
        save_path = os.path.join(path, str(i))
        if not os.path.isdir(save_path):
            os.makedirs(save_path)

        drawings = user.drawing_set.all().filter(label_index=i)

        for drawing in drawings:
            img = Image.open(drawing.image.name)
            img.save(os.path.join(save_path, drawing.name))

        save_path = os.path.join(save_path, 'data')

        if not os.path.isdir(save_path):
            os.makedirs(save_path)

    data_generation.generate_data(user_folder)


def delete_data(user_path):
    path = os.path.join(os.getcwd(), os.path.join('user_files', user_path))
    shutil.rmtree(path)
