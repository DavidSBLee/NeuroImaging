import dicom
import os
import pandas as pd

data_dir = "/Users/SB/Desktop/ML/CNN_TF/midus3_dicoms/"
patients = sorted((os.listdir(data_dir)))
labels_df = pd.read_csv("/Users/SB/Desktop/ML/CNN_TF/midus3_age.csv", index_col=0)

patients
#labels_df.head(3)

for patient in patients:
    label = labels_df.get_value(int(patient), 'Age')
    path = data_dir + str(patient)
    slices = [dicom.read_file(path + "/" + s, force=True) for s in os.listdir(path) if s[-4:] == ".dcm"]
    #slices.sort(key = lambda x: int(x.ImagePositionPatient[2]))
    print(len(slices), label)
    print(slices[0].pixel_array.shape)


len(patients)

import matplotlib.pyplot as plt
import cv2
import numpy as np
import math

IMG_PX_SIZE = 50
HM_SLICES = 20

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def mean(l):
    return sum(l)/len(l)


def process_data(patient, lebels_df, img_px_size=50, hm_slices=20, visualize=False):
    #for patient in patients:
    label = labels_df.get_value(int(patient), 'Age')
    path = data_dir + str(patient)
    slices = [dicom.read_file(path + "/" + s, force=True) for s in os.listdir(path) if s[-4:] == ".dcm"]

    new_slices = []
    slices = [cv2.resize(np.array(each_dicom.pixel_array),(IMG_PX_SIZE, IMG_PX_SIZE)) for each_dicom in slices]

    chunk_sizes = math.ceil(len(slices)/HM_SLICES) # ceil = ceiling (반올림), floor = floor(버림)
    #print (chunk_sizes)

    for slice_chunk in chunks(slices, chunk_sizes):
        slice_chunk = list(map(mean, zip(*slice_chunk)))
        new_slices.append(slice_chunk)

    print("size of reszied dicom image: " + str(len(new_slices)))

    """
    # In case slices come in different numbers
    if len(new_slices) == HM_SLICES-1:
        new_slices.append(new_slices[-1])
    if len(new_slices) == HM_SLICES-2:
        new_slices.append(new_slices[-1])
        new_slices.append(new_slices[-1])
    """
    if visualize:
        fig = plt.figure()
        for num, each_dicom in enumerate(new_slices):
            y = fig.add_subplot(4,5,num + 1)
            #new_img = cv2.resize(np.array(each_dicom.pixel_array),(IMG_PX_SIZE, IMG_PX_SIZE))
            y.imshow(new_img, cmap='gray')                                                                 
        plt.show()

    if label == 1: label = np.array([0,1])
    elif label == 0: label = np.array([1,0])

    return np.array(new_slices), label


much_data = []
for num, patient in enumerate(patients):
    print("subject number:",num + 1)
    # Every 100th subject, print the number (As a checker)
    if (num+1)/100 == 1:
        print("hitting", num+1, "subjects")
    try:
        img_data, label = process_data(patient, labels_df, img_px_size = IMG_PX_SIZE, hm_slices=HM_SLICES)
        much_data.append([img_data, label])
    except KeyError as e:
        print('This is unlabeled data')
np.save('/Users/SB/Desktop/muchdata_{}_{}_{}.npy'.format(IMG_PX_SIZE, IMG_PX_SIZE, HM_SLICES), much_data)

### Build Convolutional Neural Network
import tensorflow as tf
import numpy as np

IMG_SIZE_PX = 50
SLICE_COUNT = 20

n_classes = 2

x = tf.placeholder('float')
y = tf.placeholder('float')

keep_rate = 0.8
keep_prob = tf.placeholder(tf.float32)

def conv3d(x, W):
    return tf.nn.conv3d(x, W, strides=[1,1,1,1,1], padding='SAME')

def maxpool3d(x):
    #                        size of window         movement of window
    return tf.nn.max_pool3d(x, ksize=[1,2,2,2,1], strides=[1,2,2,2,1], padding='SAME')



def convolutional_neural_network(x):
    weights = {'W_conv1':tf.Variable(tf.random_normal([3,3,3,1,32])),
               'W_conv2':tf.Variable(tf.random_normal([3,3,3,32,64])),
               'W_fc':tf.Variable(tf.random_normal([54080,1024])),
               'out':tf.Variable(tf.random_normal([1024, n_classes]))}

    biases = {'b_conv1':tf.Variable(tf.random_normal([32])),
               'b_conv2':tf.Variable(tf.random_normal([64])),
               'b_fc':tf.Variable(tf.random_normal([1024])),
               'out':tf.Variable(tf.random_normal([n_classes]))}

    x = tf.reshape(x, shape=[-1, IMG_SIZE_PX, IMG_SIZE_PX, SLICE_COUNT, 1])

    conv1 = tf.nn.relu(conv3d(x, weights['W_conv1']) + biases['b_conv1'])
    conv1 = maxpool3d(conv1)
    
    conv2 = tf.nn.relu(conv3d(conv1, weights['W_conv2']) + biases['b_conv2'])
    conv2 = maxpool3d(conv2)

    fc = tf.reshape(conv2,[-1, 54080])
    fc = tf.nn.relu(tf.matmul(fc, weights['W_fc'])+biases['b_fc'])
    fc = tf.nn.dropout(fc, keep_rate)

    output = tf.matmul(fc, weights['out'])+biases['out']

    return output

def train_neural_network(x):
    
    much_data = np.load('/Users/SB/Desktop/muchdata_50_50_20.npy')
    train_data = much_data[:-15]
    validation_data = much_data[0:10]
    
    prediction = convolutional_neural_network(x)
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction,labels=y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    hm_epochs = 5
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for data in train_data:
                X = data[0]
                Y = data[1]
            #for _ in range(int(mnist.train.num_examples/batch_size)):
            #epoch_x, epoch_y = mnist.train.next_batch(batch_size)
                _, c = sess.run([optimizer, cost], feed_dict={x: X, y: Y})
                epoch_loss += c

            print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss)
            #print('Accuracy:',accuracy.eval({x:[i[0] for i in validation_data], y:[i[1] for i in validation_data]}))
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:',accuracy.eval({x:[i[0] for i in validation_data], y:[i[1] for i in validation_data]}))

train_neural_network(x)

