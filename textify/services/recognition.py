import pickle
import after_response
from textify.models import User
from textify.core.text_converter import TextConverter
from textify.exceptions import *
from textify.utils.fill import *
import threading
import textify.utils.classification as classification
from textify.core.data_collectors import *
import textify.core.handwritten_rec as handwritten_rec


def textify(img):
    filename = os.path.join('user_files', str(uuid.uuid4()) + '.png')
    img.save(filename)
    text = TextConverter.convert(filename)
    os.remove(filename)
    return text


def schedule_training(user_id):
    try:
        user = User.objects.get(pk=user_id)
        if user.training_machine:
            raise MachineCurrentlyTrainingException('Machine is currently being trained!')
        else:
            user.training_machine = True
            user.save(update_fields=["training_machine"])
            train_machine.after_response(user)
            return True
    except User.DoesNotExist:
        raise UserDoesNotExistException("User does not exist!")


def check_for_completion(user_id):
    try:
        user = User.objects.get(pk=user_id)

        if user.training_machine:
            raise MachineCurrentlyTrainingException('Machine is currently being trained!')
        else:
            return True
    except User.DoesNotExist:
        raise UserDoesNotExistException("User does not exist!")


@after_response.enable
def train_machine(user):
    folder_name = str(uuid.uuid4())
    fill_drawings(user)
    user.classificationmachine_set.all().delete()
    get_data(user, folder_name)
    cla = classification.train_machine(folder_name)
    pickle_path = to_pickle(cla, os.path.join(os.getcwd(), os.path.join('user_files', 'classifiers')))
    user.classificationmachine_set.create(pickle=pickle_path)
    user.training_machine = False
    user.save(update_fields=["training_machine"])
    delete_data(folder_name)


def textify_handprinted(user_id, img):
    try:
        user = User.objects.get(pk=user_id)
        classifier_path = user.classificationmachine_set.first().pickle
    except:
        classifier_path = os.path.join(os.getcwd(), os.path.join('user_files',
                                                                 os.path.join('classifiers', 'default.pkl')))

    with open(classifier_path, 'rb') as handle:
        classifier = pickle.load(handle)

    return handwritten_rec.textify(img, classifier)


def to_pickle(object_to_dump, path):
    pickle_name = str(uuid.uuid4()) + '.pkl'
    filename = os.path.join(path, pickle_name)
    with open(filename, 'wb') as handle:
        pickle.dump(object_to_dump, handle)

    return filename
