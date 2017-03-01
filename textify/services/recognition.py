import pickle
from textify.models import User
from textify.core.text_converter import TextConverter
from textify.exceptions import *
from textify.utils.fill import *
import textify.utils.classification as classification
from textify.core.data_collectors import *
import textify.core.handwritten_rec as handwritten_rec


def textify(img):
    filename = os.path.join('user_files', str(uuid.uuid4()) + '.png')
    img.save(filename)
    text = TextConverter.convert(filename)
    os.remove(filename)
    return text


def train_machines(user_id):
    try:
        folder_name = str(uuid.uuid4())
        user = User.objects.get(pk=user_id)
        fill_drawings(user)
        user.classificationmachine_set.all().delete()
        get_data(user, folder_name)
        cla = classification.train_machine(folder_name)
        pickle_path = to_pickle(cla, os.path.join('user_files', 'classifiers'))
        user.classificationmachine_set.create(pickle=pickle_path)
        delete_data(folder_name)
    except User.DoesNotExist:
        raise UserDoesNotExistException("User does not exist")


def textify_handprinted(user_id, img):
    try:
        user = User.objects.get(pk=user_id)
        classifier_path = user.classificationmachine_set.first().pickle
    except:
        classifier_path = os.path.join('user_files', os.path.join('classifiers', 'default.pkl'))

    with open(classifier_path, 'rb') as handle:
        classifier = pickle.load(handle)

    return handwritten_rec.textify(img, classifier)


def to_pickle(object_to_dump, path):
    pickle_name = str(uuid.uuid4()) + '.pkl'
    filename = os.path.join(path, pickle_name)
    with open(filename, 'wb') as handle:
        pickle.dump(object_to_dump, handle)

    return filename
