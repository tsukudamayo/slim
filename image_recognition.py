from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import os
import sys
import time
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import tensorflow as tf

from nets import mobilenet_v1

slim = tf.contrib.slim


FLAGS = tf.app.flags.FLAGS

#-----------#
# constants #
#-----------#
_NUM_CLASSES = 3
_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_google_kurashiru_20180903_cu_ep_tm_2200_x_10'
_LABEL_DATA = 'labels.txt'
_CHECKPOINT_PATH = '/media/panasonic/644E9C944E9C611A/tmp/model/20180814_food_256_manually_select_ep_tm_cu_x10_mobilenet_v1_1_224_finetune'
_CHECKPOINT_FILE = 'model.ckpt-20000'
_IMAGE_DIR = 'image'
_LOG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/log'
fname = 'data/'


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

  eval_image = Image.open(fname)
  plt.imshow(eval_image)
  plt.show()

  tf.reset_default_graph()
  
  file_input = tf.read_file(fname)
  input = tf.image.decode_png(tf.read_file(file_input), channels=3)
  images = tf.expand_dims(input, 0)
  # images = tf.cast(images, tf.float32)/128 - 1
  images.set_shape((None, None, None, 3))
  images = tf.image.resize_images(images, (224,224))

  with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
    logits, end_points = mobilenet_v1.mobilenet_v1(
        images,
        num_classes=_NUM_CLASSES,
        is_training=False,
    )
    
  vars = slim.get_variables_to_restore()
  saver = tf.train.Saver()

  #------------#
  # prediction #
  #------------#
  with tf.Session() as sess:
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


if __name__ == '__main__':
  main()
