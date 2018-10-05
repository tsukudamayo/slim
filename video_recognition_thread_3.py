from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
from datetime import datetime
import threading
import requests

import numpy as np
import cv2
import tensorflow as tf

from nets import mobilenet_v1

slim = tf.contrib.slim

FLAGS = tf.app.flags.FLAGS

_URL = 'http://localhost:8080/update_recipe'
_LOG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/log'

#---------------------#
# ingredient property #
#---------------------#
_INGREDIENT_NUM_CLASSES = 12
_INGREDIENT_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_google_search_224_20180925_x_10'
_INGREDIENT_LABEL_DATA = 'labels.txt'
_INGREDIENT_DB_DATA = 'labels_db.txt'
_INGREDIENT_CHECKPOINT_PATH = '/media/panasonic/644E9C944E9C611A/tmp/model/20180925_food_google_search_224_12class_x_10_mobilenet_v1_1_224_finetune'
_INGREDIENT_CHECKPOINT_FILE = 'model.ckpt-20000'

#------------------#
# cooking property #
#------------------#
_COOKING_NUM_CLASSES = 7
_COOKING_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/cooking_kurashiru_20180926_x_10'
_COOKING_LABEL_DATA = 'labels.txt'
# _COOKING_DB_DATA = 'labels_db.txt'
_COOKING_CHECKPOINT_PATH = '/media/panasonic/644E9C944E9C611A/tmp/model/20180926_cooking_kurashiru_224_x_10_mobilenet_v1_1_224_finetune'
_COOKING_CHECKPOINT_FILE = 'model.ckpt-20000'

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
        try:
            key = int(key_value[0])
        except KeyError:
            key = key_value[0]
        except ValueError:
            key = str(key_value[0])
        value = key_value[1].split()[0] # delete linefeed
        category_map[key] = value
    
    return category_map


def print_coordinates(event, x, y, flags, param):
  """get the coordinates when left mouse button clicked"""
  print(x, y)


def settings_property():
    # #--------------------#
    # # property of opencv #
    # #--------------------#
    # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    # contrast = cap.get(cv2.CAP_PROP_CONTRAST)
    # saturation = cap.get(cv2.CAP_PROP_SATURATION)
    # hue = cap.get(cv2.CAP_PROP_HUE)
    # # gain = cap.get(cv2.CAP_PROP_GAIN) # gain is not supported 
    # exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    # rectification = cap.get(cv2.CAP_PROP_RECTIFICATION)

    # monochrome = cap.get(cv2.CAP_PROP_MONOCHROME)
    # sharpness = cap.get(cv2.CAP_PROP_SHARPNESS)
    # auto_exposure = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
    # gamma = cap.get(cv2.CAP_PROP_GAMMA)
    # temperture = cap.get(cv2.CAP_PROP_TEMPERATURE)
    # white_blance = cap.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V)
    # zoom = cap.get(cv2.CAP_PROP_ZOOM)
    # focus = cap.get(cv2.CAP_PROP_FOCUS)
    # guid = cap.get(cv2.CAP_PROP_GUID)
    # iso_speed = cap.get(cv2.CAP_PROP_ISO_SPEED)
    # backlight = cap.get(cv2.CAP_PROP_BACKLIGHT)
    # pan = cap.get(cv2.CAP_PROP_PAN)
    # tilt = cap.get(cv2.CAP_PROP_TILT)
    # roll = cap.get(cv2.CAP_PROP_IRIS)
    
    # #----------------#
    # # property debug #
    # #----------------#
    # print('width', width)
    # print('height', height)
    # print('fps', fps)
    # print('brightness', brightness)
    # print('contrast', contrast)
    # print('saturation', saturation)
    # print('hue', hue)
    # # print('gain', gain) # gain is not supported
    # print('exposure', exposure)
    # print('hue', hue)
    # print('exposure', exposure)
    # print('rectification', rectification)
    # print('monochrome', monochrome)
    # print('sharpness', sharpness)
    # print('auto_exposure', auto_exposure)
    # print('gamma', gamma)
    # print('temperture', temperture)
    # print('white_blance', white_blance)
    # print('zoom', zoom)
    # print('focus', focus)
    # print('guid', guid)
    # print('iso_speed', iso_speed)
    # print('backlight', backlight)
    # # print('pan', pan)
    # # print('tilt', tilt)
    # # print('roll', roll)
    return


class ingredient_thread(threading.Thread):
  def __init__(self,
               bbox2,
               bbox3,
               output_dir,
               checkpoint_file,
               category_map,
               db_map,
               previous_predictions_1,):
    super(ingredient_thread, self).__init__()
    self.bbox2 = bbox2
    self.bbox3 = bbox3
    self.output_dir = output_dir
    self.checkpoint_file = checkpoint_file
    self.category_map = category_map
    self.db_map = db_map
    self.previous_predictions_1 = previous_predictions_1
    self.current_predictions_1 = []
    
  def run(self):
    tf.reset_default_graph()
    
    # file_input = tf.placeholder(tf.string, ())
    # input = tf.image.decode_png(tf.read_file(file_input))
    input = tf.placeholder('float', [None,None,3])
    images = tf.expand_dims(input, 0)
    images = tf.cast(images, tf.float32)/128 - 1
    images.set_shape((None,None,None,3))
    images = tf.image.resize_images(images,(224,224))

    with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
      logits, end_points = mobilenet_v1.mobilenet_v1(
          images,
          num_classes=_INGREDIENT_NUM_CLASSES,
          is_training=False,
      )
      
    vars = slim.get_variables_to_restore()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
      bbox2 = self.bbox2[:,:,::-1]
      bbox3 = self.bbox3[:,:,::-1]
      
      # evaluation
      log = str()
      all_bbox = [bbox2, bbox3]
      bbox_names = ['left', 'right']
      for bbox, bbox_name in zip(all_bbox, bbox_names):
        saver.restore(sess, self.checkpoint_file)
        x = end_points['Predictions'].eval(
            feed_dict={input: bbox}
        )
        # output top predicitons
        if bbox_name == 'left':
            print('*'*20 + 'LEFT' + '*'*20)
        elif bbox_name == 'right':
            print('*'*20 + 'RIGHT' + '*'*20)
        print(sys.stdout.write(
            '%s Top 1 prediction: %d %s %f'
            % (str(bbox_name), x.argmax(), self.category_map[x.argmax()], x.max())
        ))

        # output all class probabilities
        for i in range(x.shape[1]):
          print(sys.stdout.write('%s : %s' % (self.category_map[i], x[0][i])))

        pred_id = self.db_map[self.category_map[x.argmax()]]

        self.current_predictions_1.append(pred_id)

        # send GET request if prediction is changed
      # send_get_request(_URL, 'gradient', self.category_map[x.argmax()])
      # print('send GET')
      # print('time :', datetime.now().strftime('%Y%m%d:%H%M%S'))
      # prediction_category = x.argmax()
      # requests.get('http://localhost:8080/update_recipe?ingredient_ids=42,46&ingredient_ids2=43,617&flying_pan=true&page_index=0')
      print('self.previous_predictions_1', self.previous_predictions_1)
      print('self.current_predictions_1', self.current_predictions_1)
      print(self.previous_predictions_1 == self.current_predictions_1)
      if self.previous_predictions_1 != self.current_predictions_1:
        print('change')
        t_query_0 = time.time()
        query = 'http://localhost:8080/update_recipe?ingredient_ids1={}&ingredient_ids2={}&flying_pan=true'.format(
            self.current_predictions_1[0],
            self.current_predictions_1[1],
        )
        # # query = 'http://localhost:3000?ingredient_ids={0}&ingredient_ids2={1}&flying_pan=true'.format(
        # #     current_predictions_1[0],
        # #     current_predictions_1[1],
        # # )
        requests.get(query)
        t_query_1 = time.time()
        print('request time :', t_query_1 - t_query_0)
      else:
        print('not change')
        pass


class cooking_thread(threading.Thread):
  def __init__(self,
               bbox1,
               output_dir,
               checkpoint_file,
               category_map,
               # db_map,
               previous_predictions_2,):
    super(cooking_thread, self).__init__()
    self.bbox1 = bbox1
    self.output_dir = output_dir
    self.checkpoint_file = checkpoint_file
    self.category_map = category_map
    # self.db_map = db_map
    self.previous_predictions_2 = previous_predictions_2
    self.current_predictions_2 = []
    
  def run(self):
    tf.reset_default_graph()
    
    # file_input = tf.placeholder(tf.string, ())
    # input = tf.image.decode_png(tf.read_file(file_input))
    input = tf.placeholder('float', [None,None,3])
    images = tf.expand_dims(input, 0)
    images = tf.cast(images, tf.float32)/128 - 1
    images.set_shape((None,None,None,3))
    images = tf.image.resize_images(images,(224,224))

    with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
      logits, end_points = mobilenet_v1.mobilenet_v1(
          images,
          num_classes=_COOKING_NUM_CLASSES,
          is_training=False,
      )
      
    vars = slim.get_variables_to_restore()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
      bbox1 = self.bbox1[:,:,::-1]
      
      # evaluation
      log = str()
      bbox = bbox1
      saver.restore(sess, self.checkpoint_file)
      x = end_points['Predictions'].eval(
          feed_dict={input: bbox}
      )
      print(sys.stdout.write(
          'x.argmax() : ' % x.argmax()
      ))
      # output top predicitons
      print(sys.stdout.write(
          'Top 1 prediction: %d %s %f'
          % (x.argmax(), self.category_map[x.argmax()], x.max())
      ))

      # output all class probabilities
      for i in range(x.shape[1]):
        print(sys.stdout.write('%s : %s' % (self.category_map[i], x[0][i])))

      # requests
      # pred_id = self.db_map[self.category_map[x.argmax()]]

      # self.current_predictions_2.append(pred_id)

      # print('self.previous_predictions_2', self.previous_predictions_2)
      # print('self.current_predictions_2', self.current_predictions_2)
      # print(self.previous_predictions_2 == self.current_predictions_2)
      # if self.previous_predictions_2 != self.current_predictions_2:
      #   print('change')
      #   t_query_0 = time.time()
      #   query = 'http://localhost:8080/update_recipe?ingredient_ids1={}&ingredient_ids2={}&flying_pan=true'.format(
      #       self.current_predictions_2[0],
      #       self.current_predictions_2[1],
      #   )
      #   requests.get(query)
      #   t_query_1 = time.time()
      #   print('request time :', t_query_1 - t_query_0)
      # else:
      #   print('not change')
      #   pass


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
  ingredient_checkpoint_file = os.path.join(
      _INGREDIENT_CHECKPOINT_PATH, _INGREDIENT_CHECKPOINT_FILE
  )
  ingredient_category_map = convert_label_files_to_dict(
      _INGREDIENT_DATA_DIR, _INGREDIENT_LABEL_DATA
  )

  cooking_checkpoint_file = os.path.join(
      _COOKING_CHECKPOINT_PATH, _COOKING_CHECKPOINT_FILE
  )
  cooking_category_map = convert_label_files_to_dict(
      _COOKING_DATA_DIR, _COOKING_LABEL_DATA
  )
  
  db_map = convert_label_files_to_dict(
      _INGREDIENT_DATA_DIR, _INGREDIENT_DB_DATA
  )

  #-----------------------------#
  # videocapture and prediction #
  #-----------------------------#
  width = 1920
  height = 1080

  # define ROI
  threshold = int(224 / 2)                         # default (224 / 2)
  margin = 10                                      # not to capture bounding box

  center = int(width * 6.0/10)
  center1_width = int(center - (threshold*2 + margin)) # ROI1 center x
  center2_width = int(center)                          # ROI2 center x
  center3_width = int(center + (threshold*2 + margin)) # ROI2 center x
  center_height = int(height / 2)                  # ROI1,2 center y

  # print('center1_width :', center1_width)
  # print('center2_width :', center2_width)
  # print('center_height :', center_height)
  
  cap = cv2.VideoCapture(0)

  # camera propety(1920x1080)
  cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  # requests.get('http://localhost:8080/update_recipe?ingredient_ids1=42,46&ingredient_ids2=43,617&frying_pan=true&page_index=0')
  
  # start video capture
  count = 0
  previous_predictions_1 = []
  previous_predictions_2 = []
  t1 = time.time()
  print('start ~ while :', t1 - t0)
  while(True):
    t3 = time.time()
    ret, frame = cap.read()
    share_margin = int(margin/2)
    cv2.rectangle(
        frame,
        ((center1_width-threshold-(share_margin)),
         (center_height-threshold-(share_margin))), # start coordinates
        ((center1_width+threshold+(share_margin)),
         (center_height+threshold+(share_margin))), # end coordinates
        (0,0,255),
        3
    )
    cv2.rectangle(
        frame,
        ((center2_width-threshold-(share_margin)),
         (center_height-threshold-(share_margin))), # start coordinates
        ((center2_width+threshold+(share_margin)),
         (center_height+threshold+(share_margin))), # end coordinates 
        (0,0,255),
        3
    )
    cv2.rectangle(
        frame,
        ((center3_width-threshold-(share_margin)),
         (center_height-threshold-(share_margin))), # start coordinates
        ((center3_width+threshold+(share_margin)),
         (center_height+threshold+(share_margin))), # end coordinates
        (0,0,255),
        3
    )

    cv2.imshow('frame', frame)
    # cv2.setMouseCallback('frame', print_coordinates)

    # ROI
    bbox1 = frame[center_height-threshold:center_height+threshold,
                  center1_width-threshold:center1_width+threshold]
    bbox2 = frame[center_height-threshold:center_height+threshold,
                  center2_width-threshold:center2_width+threshold]
    bbox3 = frame[center_height-threshold:center_height+threshold,
                  center3_width-threshold:center3_width+threshold]

    # save image of bounding box
    now = datetime.now()
    seconds = now.strftime('%Y%m%d_%H%M%S') + '_' + str(now.microsecond)
    cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox1.png', bbox1)
    cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox2.png', bbox2)
    cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox3.png', bbox3)

    # # BGR t0 RGB
    # bbox1 = bbox1[:,:,::-1]
    # bbox2 = bbox2[:,:,::-1]
    # bbox3 = bbox3[:,:,::-1]

    if count % 20 == 0:
      thread1 = ingredient_thread(
          bbox2,
          bbox3,
          output_dir,
          ingredient_checkpoint_file,
          ingredient_category_map,
          db_map,
          previous_predictions_1,
        )
      thread1.start()
      previous_predictions_1 = thread1.current_predictions_1
    elif count % 20 == 11:
      thread2 = cooking_thread(
          bbox1,
          output_dir,
          cooking_checkpoint_file,
          cooking_category_map,
          # db_map,
          previous_predictions_2,
        )
      thread2.start()
      previous_predictions_2 = thread2.current_predictions_2
          
    else:
      pass    

    t4 = time.time()
    print('loop seconds :', t4 - t3)
            
    count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  
  cap.release()
  cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
