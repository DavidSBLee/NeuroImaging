
# coding: utf-8

# In[37]:


import nibabel as nb
import numpy as np
import glob
from scipy import ndimage as nd
import keras

path = "/Users/SB/Desktop/[0-9][0-9][0-9][0-9][0-9]/*nii.gz"
files = glob.glob(path)

empty_array = np.zeros((20,20,10))
data_array = np.zeros((256, 256, 124))
factor = [w/float(f) for w, f in zip(empty_array.shape, data_array.shape)]
print("resampling factor:", factor)

#Test for single file
#for file in files:
    #img = nb.load(file)
    #data = img.get_data()
        # or #data = img.dataobj
        #data = np.array(data)
    #print(data.shape)
    #resampled_data = nd.interpolation.zoom(data, zoom=factor)
    #resampled_data.shape
    #resampled_data.size
### Create NIfTI out of resampled data to visualize
#affine = np.diag([1, 2, 3, 1])
#array_img = nb.Nifti1Image(resampled_data, affine)
#nb.save(array_img, '/Users/SB/Desktop/array_image.nii.gz')
   


# In[38]:


x_train = []
y_train = []
input_train = "/Users/SB/Desktop/ML/CNN_Keras/midus2_nifti/input/train/*" 
input_train = glob.glob(input_train)
for input in input_train:
    if "old" in input:
        img = nb.load(input)
        data = img.get_data()
        resampled_old = nd.interpolation.zoom(data, zoom=factor)
        x_train.append(resampled_old)
        y_train.append(int(1))
    elif "young" in input:
        img = nb.load(input)
        data = img.get_data()
        resampled_young = nd.interpolation.zoom(data, zoom=factor)
        x_train.append(resampled_young)
        y_train.append(int(0))
        
x_train = np.asarray(x_train)
x_train = np.expand_dims(x_train, axis=4)
y_train = keras.utils.to_categorical(y_train, num_classes=2)
x_train.shape


# In[39]:


x_test = []
y_test = []
input_test = "/Users/SB/Desktop/ML/CNN_Keras/midus2_nifti/input/validation/*" 
input_test = glob.glob(input_test)

for input in input_test:
    if "old" in input:
        img = nb.load(input)
        data = img.get_data()
        resampled_old = nd.interpolation.zoom(data, zoom=factor)
        x_test.append(resampled_old)
        y_test.append(int(1))
    elif "young" in input:
        img = nb.load(input)
        data = img.get_data()
        resampled_young = nd.interpolation.zoom(data, zoom=factor)
        x_test.append(resampled_young)
        y_test.append(int(0))
        
x_test = np.asarray(x_test)
x_test = np.expand_dims(x_test, axis=4)
y_test = keras.utils.to_categorical(y_test, num_classes=2)
x_test.shape


# In[47]:


from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D
from keras.optimizers import SGD

### Generate dummy data
# (# of subjects, x, y, z, # of channels (3 in case of RGB))
# x_train = np.random.random((1000, 10, 10, 10, 1))
# 2 categories, (# of subjects, # of channels, num_classes= number of label)
# y_train = keras.utils.to_categorical(np.random.randint(2, size=(1000, 1)), num_classes=2)
# x_test = np.random.random((100, 10, 10, 10, 1))
# y_test = keras.utils.to_categorical(np.random.randint(2, size=(100, 1)), num_classes=2)

### Convolutional Neural Network (Four-Layer deep CNN)
model = Sequential()
# input: 10x10x10 images with 1 channels -> (10, 10, 10, 1) tensors.
# this applies 32 convolution filters (kernels) of size 2x2x2 each.
model.add(Conv3D(32, (2, 2, 2), activation='relu', input_shape=(20, 20, 10, 1)))
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
model.fit(x_train, y_train, batch_size=10, epochs=5)#, validation_split=0.1)
accuracy = model.evaluate(x_test, y_test, batch_size=10)

print ('Test Score:', accuracy)

