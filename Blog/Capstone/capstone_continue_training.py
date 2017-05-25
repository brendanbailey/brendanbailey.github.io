#Importing Libraries
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from skimage.io import imread
from IPython.display import Image
from sklearn.model_selection import train_test_split
from shutil import copyfile
import tensorflow
import datetime

from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers.convolutional import Convolution2D, MaxPooling2D, Cropping2D
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model

plt.style.use('ggplot')

#Loading Model
model_name = input("What is model path?")
number_of_epochs = int(input("Number of epochs?"))
model = load_model(model_name)

#Gathering Image Data
batch_size = 16

# this is the augmentation configuration we will use for training
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True, data_format = "channels_first")

# this is the augmentation configuration we will use for testing:
# only rescaling
test_datagen = ImageDataGenerator(rescale=1./255, data_format = "channels_first")

# this is a generator that will read pictures found in
# subfolers of 'data/train', and indefinitely generate
# batches of augmented image data
train_generator = train_datagen.flow_from_directory(
        'train_split',  # this is the target directory
        target_size=(32, 32),  # all images will be resized to 150x150
        batch_size=batch_size)

validation_generator = test_datagen.flow_from_directory(
        'val_split',
        target_size=(32, 32),
        batch_size=batch_size)

#Training Model
history = model.fit_generator(
        train_generator,
        validation_data = validation_generator,
        steps_per_epoch=(2000 // batch_size),
        epochs=number_of_epochs,
        validation_steps=(800 // batch_size))

#Saving Model
model_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
save_model_name = "models/model_%s.h5" % model_date
model.save(save_model_name)

#Making Predictions
final_test_datagen = ImageDataGenerator(rescale=1./255, data_format = "channels_first")

final_test_generator = final_test_datagen.flow_from_directory(
        'data/kaggle/test1',
        target_size=(32, 32),
        batch_size=batch_size,
        class_mode = None)
predictions = model.predict_generator(
        final_test_generator,
        steps = (2000 // batch_size))
submission_list = []
for f, prediction in zip(final_test_generator.filenames, predictions):
    submission_list.append([f.strip("test/"), prediction[0], prediction[1], prediction[2]])
submission_frame = pd.DataFrame(submission_list, columns = ["image_name","Type_1","Type_2","Type_3"])
submission_frame.to_csv("submissions/model_%s.csv" % model_date, index = False)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.savefig("submissions/model_%s.png" % model_date)
