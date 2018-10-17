from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
from datetime import datetime
import requests

import numpy as np
import tensorflow as tf
import cv2
import skimage.io
import skimage.transform

from nets import mobilenet_v1

slim = tf.contrib.slim

#-----------#
# constants #
#-----------#
_URL = 'http://localhost:3000'

_NUM_CLASSES = 8
_DATA_DIR = 'tfrecord/cooking'
_LABEL_DATA = 'labels.txt'
_CHECKPOINT_PATH = 'model/cooking'
_CHECKPOINT_FILE = 'model.ckpt-20000'
_IMAGE_DIR = 'image'
_LOG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/log'


def send_get_request(url, key, value):
    req = urllib.request.Request(
        '{}?{}'.format(
            url,
            urllib.parse.urlencode({key: value}))
    )
    urllib.request.urlopen(req)


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


def print_coordinates(event, x, y, flags, param):
  """get the coordinates when left mouse button clicked"""
  print(x, y)


def main():
  now = datetime.now()
  today = now.strftime('%Y%m%d')
  
  t0 = time.time()

  output_dir = os.path.join(_LOG_DIR, today)
  if os.path.isdir(output_dir) is False:
    os.mkdir(output_dir)
   
  #--------------#
  # define model #
  #--------------#
  checkpoint_file = os.path.join(_CHECKPOINT_PATH, _CHECKPOINT_FILE)
  category_map = convert_label_files_to_dict(_DATA_DIR, _LABEL_DATA)

  # tf.reset_default_graph()
  eval_graph = tf.Graph()
  with eval_graph.as_default():
    
    input = tf.placeholder('float', [None,None,3])
    images = tf.expand_dims(input, 0)
    images = tf.cast(images, tf.float32)/128 - 1
    images.set_shape((None,None,None,3))
    images = tf.image.resize_images(images,(224,224))
    
    with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
      logits, end_points = mobilenet_v1.mobilenet_v1(
          images,
          num_classes=_NUM_CLASSES,
          is_training=False,
      )
    
      # ema = tf.train.ExponentialMovingAverage(0.999)
      # vars = ema.variables_to_restore()
      vars = slim.get_variables_to_restore()
      saver = tf.train.Saver()
      
      #-----------------------------#
      # videocapture and prediction #
      #-----------------------------#
      width = 1920
      height = 1080
      
      threshold = int(224 / 2) # default (224 / 2)
      margin = 10              # not to capture bounding box

      # # higobashi
      # center_width = int((width / 2)*1.03)
      # center_height = int((height / 2)*1.1)
      # kusatsu IH
      center_width = 670
      center_height = 720      
      
      
      with tf.Session(graph=eval_graph) as sess:
        cap = cv2.VideoCapture('/media/panasonic/644E9C944E9C611A/tmp/data/mov/20180907/20180907_紀文-羽根つき餃子-出来上がり.mp4')
      
        # camera propety(1920x1080)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
      
        # initalize prediction category
        previous_prediction = -1 # this number is not include category map
        status = 0

        count = 0
        # start video capture
        while(True):
          ret, frame = cap.read()
          
          cv2.rectangle(
              frame,
              ((center_width-threshold-margin),(center_height-threshold-margin)),
              ((center_width+threshold+margin),(center_height+threshold+margin)),
              (0,0,255),
              3
          )
          cv2.imshow('frame', frame)
          cv2.setMouseCallback('frame', print_coordinates)
      
          # ROI
          bbox = frame[center_height-threshold:center_height+threshold,
                       center_width-threshold:center_width+threshold]
          # bbox = cv2.resize(bbox,(224,224))
      
          # save image of bounding box
          now = datetime.now()
          microseconds = now.microsecond
          seconds = str(now.strftime('%Y%m%d_%H%M%S')) + '_' + str(microseconds)
          # cv2.imwrite(os.path.join(output_dir, seconds) + '.png', bbox)
          # bbox = bbox / 128 - 1
          bbox = bbox[:,:,::-1]
          # bbox = load_image(bbox, normalize=False)
          # bbox = np.expand_dims(bbox, 0)
          # bbox = bbox.reshape((1,224,224,3))

          if count % 5 == 0:
            # evaluation          
            saver.restore(sess, checkpoint_file)
            x = end_points['Predictions'].eval(
                feed_dict={input: bbox}
            )
            
            print('previous predictions', previous_prediction)
            # print(sys.stdout.write(
            #     'currnet Top 1 prediction: %d %s %f'
            #     % (x.argmax(), category_map[x.argmax()], x.max())
            # ))
            if int(previous_prediction) + 1 == int(x.argmax()):
              status = int(x.argmax())
              previous_prediction = status
              query = 'http://localhost:8080/update_recipe?ingredient_ids1=35&ingredient_ids2=42&flying_pan=true'
              requests.get(query)
            else:
              pass
            print('current status: %s %s' % (status, category_map[status]))
            
            # if prediction_category != x.argmax():
            #   # output top predicitons
            #   print(sys.stdout.write(
            #       'Top 1 prediction: %d %s %f'
            #       % (x.argmax(), category_map[x.argmax()], x.max())
            #   ))
              # output all class probabilities
              # for i in range(x.shape[1]):
              #   print(sys.stdout.write('%s : %s' % (category_map[i], x[0][i])))
              
              # send GET request if prediction is changed
            
              # send_get_request(_URL, 'gradient', category_map[x.argmax()])
              # print('send GET')
              # print('time :', datetime.now().strftime('%Y%m%d:%H%M%S'))
              # prediction_category = x.argmax()
            
          if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
