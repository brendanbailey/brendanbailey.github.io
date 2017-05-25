import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage.io import imread
from IPython.display import Image
from shutil import copyfile
import tensorflow
import numpy as np

from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from sklearn.model_selection import GridSearchCV

from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers.convolutional import Convolution2D, MaxPooling2D, Cropping2D
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import RMSprop
from keras.models import load_model
from keras import losses

plt.style.use('ggplot')

model = Sequential()
#Adding cropping
model.add(Cropping2D(cropping=25, data_format="channels_first", input_shape=(3, 150, 150)))

#Conv Set 1
model.add(Conv2D(12, (3, 3), data_format = "channels_first"))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_first"))
model.add(Dropout(0.25))

#Conv Set 2
model.add(Conv2D(25, (3, 3), data_format="channels_first"))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2), data_format="channels_first"))
model.add(Dropout(0.25))

#FC Set 1
model.add(Flatten())
model.add(Dense(25))
model.add(Activation('tanh'))

#Final FC
model.add(Dense(3))
model.add(Activation('softmax'))

model.compile(loss=losses.categorical_crossentropy,
              optimizer='adamax',
              metrics=['categorical_accuracy'])

batch_size = 16

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        rescale=1./255, data_format = "channels_first")

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255, data_format = "channels_first")

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        'train_split',  # this is the target directory
        target_size=(150, 150),  # all images will be resized to 2000x2000
        batch_size=batch_size)

validation_generator = test_datagen.flow_from_directory(
        'val_split',
        target_size=(150, 150),
        batch_size=batch_size)

history = model.fit_generator(
        train_generator,
        validation_data = validation_generator,
        steps_per_epoch=(2000 // batch_size),
        epochs=30,
        validation_steps=(800 // batch_size))

model.save("models/whygodwhy_20170523.h5")

final_test_datagen = ImageDataGenerator(rescale=1./255, data_format = "channels_first")

final_test_generator = final_test_datagen.flow_from_directory(
        'data/kaggle/test1',
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode = None)

predictions = model.predict_generator(
        final_test_generator,
        steps = (2000 // batch_size))

submission_list = []
for f, prediction in zip(final_test_generator.filenames, predictions):
    submission_list.append([f.strip("test/"), prediction[0], prediction[1], prediction[2]])
submission_frame = pd.DataFrame(submission_list, columns = ["image_name","Type_1","Type_2","Type_3"])
submission_frame.to_csv("submissions/whygodwhy_20170523.csv", index = False)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig("submissions/whygodwhy_20170523.png")
