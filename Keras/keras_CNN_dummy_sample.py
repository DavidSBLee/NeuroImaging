import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D
from keras.optimizers import SGD

### Generate dummy data
# (# of subjects, x, y, z, # of channels (3 in case of RGB))
x_train = np.random.random((1000, 10, 10, 10, 1))
# 2 categories, (# of subjects, # of channels, num_classes= number of label)
y_train = keras.utils.to_categorical(np.random.randint(2, size=(1000, 1)), num_classes=2)
x_test = np.random.random((100, 10, 10, 10, 1))
y_test = keras.utils.to_categorical(np.random.randint(2, size=(100, 1)), num_classes=2)

### Convolutional Neural Network (Four-Layer deep CNN)
model = Sequential()
# input: 10x10x10 images with 1 channels -> (10, 10, 10, 1) tensors.
# this applies 32 convolution filters (kernels) of size 2x2x2 each.
model.add(Conv3D(32, (2, 2, 2), activation='relu', input_shape=(10, 10, 10, 1)))
model.add(Conv3D(32, (2, 2, 2), activation='relu'))
model.add(MaxPooling3D(pool_size=(2, 2, 2)))
# Dropout after pooling with probabily of 0.25 
model.add(Dropout(0.25))

# Swtiching to 64 kernels per convolution after the first pooling layer
model.add(Conv3D(64, (2, 2, 2), activation='relu'))
model.add(Conv3D(64, (2, 2, 2), activation='relu'))
model.add(MaxPooling3D(pool_size=(2, 2, 2)))
# Dropout after pooling with probabily of 0.25 
model.add(Dropout(0.25))

### This portion is Multilayer Perceptron(MLP)
# Flatten to to 2D, apply Fully Connected Layer(FC), ReLU(with dropout), softmax
model.add(Flatten())
# Dense(256) is a fully-connected layer with 256 hidden units
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
# the FC layer of the MLP will have 2 neurons
model.add(Dense(2, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy', optimizer=sgd)

# In each iteration - consider 20 training examples at once
# num_epochs - iterate 3 times over the entire traning set
# validation_split - levae 10% of the data for validation
model.fit(x_train, y_train, batch_size=20, epochs=3, validation_split=0.1)
accuracy = model.evaluate(x_test, y_test, batch_size=100)

print ('Test Score:', accuracy)
