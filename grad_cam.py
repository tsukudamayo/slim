from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os
import sys
import time
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import skimage
import skimage.io
import skimage.transform

import cv2

import tensorflow as tf
from tensorflow.contrib.keras.api.keras.applications.mobilenet import preprocess_input
from tensorflow.python.framework import ops
from tensorflow.python.ops import gen_nn_ops

@ops.RegisterGradient('GuidedRelu')
def _GuidedReluGrad(op, grad):
    return tf.where(0. < grad,
                    gen_nn_ops._relu_grad(grad, op.outputs[0]),
                    tf.zeros(grad.get_shape()))

from nets import mobilenet_v1
from preprocessing import preprocessing_factory

slim = tf.contrib.slim


FLAGS = tf.app.flags.FLAGS

#-----------#
# constants #
#-----------#
_NUM_CLASSES = 7
_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/cooking_20180925'
_LABEL_DATA = 'labels.txt'
_CHECKPOINT_PATH = '/media/panasonic/644E9C944E9C611A/tmp/model/20180926_cooking_kurashiru_224_x_10_mobilenet_v1_1_224_finetune'
_CHECKPOINT_FILE = 'model.ckpt-20000'
_IMAGE_DIR = 'image'
_LOG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/log'
_MODEL_NAME = 'mobilenet_v1'
# fname = 'data/tomato_real_002.png'
gradient_name = 'tomato'
_VALIDATION_DIR='validation'


def load_image(path, normalize=True):
    img = skimage.io.imread(path)
    print('img.max :', img.max())
    print('img.min :', img.min())
    if normalize:
        img = img / 255.0
        print('norm img.max :', img.max())
        print('norm img.min :', img.min())
        assert (0 <= img).all() and (img <= 1.0).all()

    short_edge = min(img.shape[:2])
    yy = int((img.shape[0] - short_edge) / 2)
    xx = int((img.shape[1] - short_edge) / 2)
    crop_img = img[yy: yy + short_edge, xx: xx + short_edge]
    resized_img = skimage.transform.resize(
        crop_img,
        (224,224),
        preserve_range=True
    )

    return resized_img


def visualize(image, conv_output, conv_grad, gb_viz):
  image = np.squeeze(image, 0)
  output = np.squeeze(conv_output, 0)
  grads_val = np.squeeze(conv_grad, 0)
  gb_viz = np.squeeze(gb_viz, 0)
  print('grads_val shape :', grads_val.shape)
  print('gb_viz shape :', gb_viz.shape)

  weights = np.mean(grads_val, axis=(0,1))
  print('weights', weights.shape)
  cam = np.zeros(output.shape[0:2], dtype=np.float32)
  print('cam ', cam.shape)

  # taking a waighted average
  for i, w in enumerate(weights):
    # print('i', i)
    # print('w', w)
    # print('cam', cam)
    cam += w * output[:,:,i]

  # passing throught ReLU
  cam = np.maximum(cam, 0)
  cam = cam / np.max(cam)
  cam = skimage.transform.resize(cam, (224,224), preserve_range=True)

  img = image.astype(float)
  img -= np.min(img)
  img /= img.max()

  cam_heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
  cam_heatmap = cv2.cvtColor(cam_heatmap, cv2.COLOR_BGR2RGB)

  fig = plt.figure()
  ax = fig.add_subplot(121)
  imgplot = plt.imshow(img)
  ax.set_title('input_image')

  # TODO guided back propagation
  # ax = fig.add_subplot(132)
  # imgplot = plt.imshow(cam_heatmap)
  # ax.set_title('Grad-CAM')

  # gb_viz = np.dstack((
  #     gb_viz[:,:,0],
  #     gb_viz[:,:,1],
  #     gb_viz[:,:,2],
  # ))
  # gb_viz -= np.min(gb_viz)
  # gb_viz /= gb_viz.max()

  # ax = fig.add_subplot(132)
  # imgplot = plt.imshow(gb_viz)
  # ax.set_title('guided backpropagation')

  # gb_gb = np.dstack((
  #     gb_viz[:,:,0] * cam,
  #     gb_viz[:,:,1] * cam,
  #     gb_viz[:,:,2] * cam,
  # ))

  # ax = fig.add_subplot(223)
  # imgplot = plt.imshow(gb_gb)
  # ax.set_title('guided Grad-CAM')

  superimposed_img = cam_heatmap + img
  ax = fig.add_subplot(122)
  plt.imshow(superimposed_img)
  plt.title('guided Grad-CAM superimposed')

  plt.show()


def convert_label_files_to_dict(data_dir, label_file):
  category_map = {}
  keys, values = [], []
  
  # read label file
  with open(os.path.join(data_dir, label_file)) as f:
    lines = f.readlines()
    f.close()

  # label file convert into python dictionary
  for line in lines:
    key_value = line.split(':')
    key = int(key_value[0])
    value = key_value[1].split()[0] # delete linefeed
    category_map[key] = value
  
  return category_map


def main():
  now = datetime.now()
  today = now.strftime('%Y%m%d')

  t0 = time.time()

  output_dir = os.path.join(_LOG_DIR, today)
  if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)

  #--------------#
  # difine model #
  #--------------#
  checkpoint_file = os.path.join(_CHECKPOINT_PATH, _CHECKPOINT_FILE)
  category_map = convert_label_files_to_dict(_DATA_DIR, _LABEL_DATA)
  
  validation_files = []
  for root, dirs, files in os.walk(_VALIDATION_DIR):
    for f in files:
      filepath = os.path.join(root, f)
      validation_files.append(filepath)
  
  for fname in validation_files:
  
    eval_graph = tf.Graph()
    with eval_graph.as_default():
      with eval_graph.gradient_override_map({'Relu': 'Guidedrelu'}):
        
        # tf.reset_default_graph()
    
        file_input = tf.read_file(fname)
        input = tf.image.decode_png(tf.read_file(file_input), channels=3)
        images = tf.expand_dims(input, 0)
        images = tf.cast(images, tf.float32)/128 - 1
        images.set_shape((None, None, None, 3))
        images = tf.image.resize_images(images, (224,224))
        print('images = resize_images', images)
    
        labels = tf.placeholder(tf.float32, [1, _NUM_CLASSES])
        
        with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
          logits, end_points = mobilenet_v1.mobilenet_v1(
              images,
              num_classes=_NUM_CLASSES,
              is_training=False,
          )
          
        prob = end_points['Predictions']
        cost = (-1) * tf.reduce_sum(tf.multiply(labels, tf.log(prob)), axis=1)
        print('cost: ', cost)
    
        y_c = tf.reduce_sum(tf.multiply(logits, labels), axis=1)
        print('reduce_sum(logits, labels)', y_c)
    
        target_conv_layer = end_points['Conv2d_13_pointwise']
        target_conv_layer_grad = tf.gradients(y_c, target_conv_layer)[0]
    
        gb_grad = tf.gradients(cost, images)[0]
          
        vars = slim.get_variables_to_restore()
        saver = tf.train.Saver()
    
    
    eval_image = load_image(fname, normalize=False)
    eval_image = eval_image.reshape((1,224,224,3))
    
    # category_number = category_map[gradient_name]
    eval_label = np.array([1 if i == 0 else 0 for i in range(_NUM_CLASSES)])
    eval_label = eval_label.reshape(1, -1)
    
    #------------#
    # prediction #
    #------------#
    with tf.Session(graph=eval_graph) as sess:
      saver.restore(sess, checkpoint_file)
      x = end_points['Predictions'].eval(
          feed_dict={file_input: fname}
      )
    
      # output top predicitions
      print(sys.stdout.write('Top 1 prediction: %d %s %f'
                  % (x.argmax(), category_map[x.argmax()], x.max())))
      
      # output all class probabilities
      for i in range(x.shape[1]):
          print(sys.stdout.write('%s : %s' % (category_map[i], x[0][i])))
    
      # visualize hidden layer
      # print('end_points\n', end_points)
    
      gb_grad_val, target_conv_layer_val, target_conv_layer_grad_val = sess.run(
          [gb_grad, target_conv_layer, target_conv_layer_grad],
          feed_dict={images: eval_image, labels: eval_label}
          )
      print('gb_grad_val.shape', gb_grad_val.shape)
      print('target_conv_layer_val.shape', target_conv_layer_grad_val.shape)
      print('target_conv_layer_grad_val.shape', target_conv_layer_grad_val.shape)
    
      visualize(eval_image,
                target_conv_layer_val,
                target_conv_layer_grad_val,
                gb_grad_val)


if __name__ == '__main__':
  main()
