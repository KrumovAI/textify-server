import os
from random import shuffle
import numpy
from sklearn import svm, metrics
from PIL import Image


def train_machine(user_path):
    images = []
    test = []

    print("======COLLECTING DATA======")
    for i in range(0, 26):
        path = os.path.join(os.getcwd(), 'user_files')
        path = os.path.join(path, user_path)
        path = os.path.join(path, 'handwritten/' + str(i) + '/data')
        counter = 0
        files = os.listdir(path)
        shuffle(files)

        for f in range(int(len(files))):
            file = files[f]

            if file == "Thumbs.db":
                continue

            images.append([numpy.array(Image.open(path + '\\' + file).convert('L')), i])
            counter += 1

    shuffle(images)
    shuffle(test)
    target = []
    data = []

    for k in range(len(images)):
        target.append(images[k][1])
        data.append(images[k][0])

    print(len(data))

    data = numpy.reshape(data, (len(data), -1))
    classifier = svm.LinearSVC(loss='hinge', multi_class="ovr", C=0.00001)

    print("=======TRAINING DATA=======")

    train_data = data[0:int(len(data) / 2)]
    train_target = target[0:int(len(target) / 2)]
    classifier.fit(train_data, train_target)

    # Now predict the value of the digit on the second half:
    expected = target[int(len(target) / 2):]
    predicted = classifier.predict(data[int(len(target) / 2):])

    print("Classification report for classifier %s:\n%s\n"
          % (classifier, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

    # plt.scatter(predicted, expected)
    # plt.show()

    print("=====SAVING CLASSIFIER=====")
    return classifier

