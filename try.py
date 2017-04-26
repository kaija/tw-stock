import numpy as np
from keras.utils import np_utils
nb_classes = 10
labels = np.random.randint(2, size=(20, 1))
print labels
test = np_utils.to_categorical(labels, nb_classes)
print test
