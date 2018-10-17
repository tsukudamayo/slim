from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
from datetime import datetime
import threading
# import concurrent.futures
import requests
import numpy as np
import cv2
import tensorflow as tf

from nets import mobilenet_v1

slim = tf.contrib.slim

FLAGS = tf.app.flags.FLAGS

_URL = 'http://localhost:8080/update_recipe'
# _LOG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/log'

#---------------------#
# ingredient property #
#---------------------#
_INGREDIENT_NUM_CLASSES = 18
_INGREDIENT_DATA_DIR = 'tfrecord/ingredient/'
_INGREDIENT_LABEL_DATA = 'labels.txt'
_INGREDIENT_DB_DATA = 'labels_db.txt'
_INGREDIENT_CHECKPOINT_PATH = 'model/ingredient'
_INGREDIENT_CHECKPOINT_FILE = 'model.ckpt-20000'

#------------------#
# cooking property #
#------------------#
_COOKING_NUM_CLASSES = 8
_COOKING_DATA_DIR = 'tfrecord/cooking'
_COOKING_LABEL_DATA = 'labels.txt'
# _COOKING_DB_DATA = 'labels_db.txt'
_COOKING_CHECKPOINT_PATH = 'model/cooking'
_COOKING_CHECKPOINT_FILE = 'model.ckpt-20000'

#------------------#
# cookware property #
#------------------#
_COOKWARE_NUM_CLASSES = 4
_COOKWARE_DATA_DIR = 'tfrecord/cookware'
_COOKWARE_LABEL_DATA = 'labels.txt'
# _COOKWARE_DB_DATA = 'labels_db.txt'
_COOKWARE_CHECKPOINT_PATH = 'model/cookware'
_COOKWARE_CHECKPOINT_FILE = 'model.ckpt-20000'


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


class IngredientThread(threading.Thread):
  def __init__(self,
               bbox3,
               bbox4,
               # output_dir,
               checkpoint_file,
               category_map,
               db_map,
               previous_predictions_1,
               bbox3_instances,
               bbox4_instances,
               current_instances,
               bbox3_category,
               bbox4_category):
    super(IngredientThread, self).__init__()
    self.bbox3 = bbox3
    self.bbox4 = bbox4
    # self.output_dir = output_dir
    self.checkpoint_file = checkpoint_file
    self.category_map = category_map
    self.db_map = db_map
    self.previous_predictions_1 = previous_predictions_1
    self.current_predictions_1 = []
    self.bbox3_instance = bbox3_instances
    self.bbox4_instance = bbox4_instances
    self.current_instances = []
    self.bbox3_category = bbox3_category
    self.bbox4_category = bbox4_category
    
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
      bbox3 = self.bbox3[:,:,::-1]
      bbox4 = self.bbox4[:,:,::-1]
      
      # evaluation
      log = str()
      all_bbox = [bbox3, bbox4]
      bbox_names = ['left', 'right']
      self.current_instances = []
      recognition_rates = []
      for bbox, bbox_name in zip(all_bbox, bbox_names):
        saver.restore(sess, self.checkpoint_file)
        x = end_points['Predictions'].eval(
            feed_dict={input: bbox}
        )
        # output top predicitons
        if bbox_name == 'left':
            print('*'*20 + 'LEFT' + '*'*20)
            self.current_instances.append(self.category_map[x.argmax()])
            category_name = str(self.category_map[x.argmax()])
            probability = '{:.4f}'.format(x.max())
            self.bbox3_instance = str(category_name) + ' : ' + probability
            recognition_rates.append(x.max())
            self.bbox3_category = self.category_map[x.argmax()]
        elif bbox_name == 'right':
            print('*'*20 + 'RIGHT' + '*'*20)
            self.current_instances.append(self.category_map[x.argmax()])
            category_name = str(self.category_map[x.argmax()])
            probability = '{:.4f}'.format(x.max())
            self.bbox4_instance = str(category_name) + ' : ' + probability
            recognition_rates.append(x.max())
            self.bbox4_category = self.category_map[x.argmax()]
        print(sys.stdout.write(
            '%s Top 1 prediction: %d %s %f'
            % (str(bbox_name), x.argmax(), self.category_map[x.argmax()], x.max())
        ))

        # output all class probabilities
        for i in range(x.shape[1]):
          print(sys.stdout.write('%s : %s' % (self.category_map[i], x[0][i])))

        pred_id = self.db_map[self.category_map[x.argmax()]]

        self.current_predictions_1.append(pred_id)

      print('current_instances', self.current_instances)
      print('self.bbox3_instance', self.bbox3_instance)
      print('self.bbox4_instance', self.bbox4_instance)

      if self.previous_predictions_1[0] is '':
        self.previous_predictions_1[0] = '0'
      if self.previous_predictions_1[1] is '':
        self.previous_predictions_1[1] = '0'

      print('self.current_predictions_1', type(self.current_predictions_1[0]))

      print('self.previous_predictions_1', self.previous_predictions_1)
      print('self.current_predictions_1', self.current_predictions_1)
      print(self.previous_predictions_1 != self.current_predictions_1)

      # send request when it detects changing ingredients
      if self.previous_predictions_1 != self.current_predictions_1:
        print('change')
        print('*'*15 + ' request ' +'*'*15)
        t_query_0 = time.time()
        
        if self.current_predictions_1[0] == '0' and self.current_predictions_1[1] == '0':
          self.current_predictions_1[0] = '0'
          self.current_predictions_1[1] = '0'
        if self.current_predictions_1[0] == '0' and self.current_predictions_1[1] is not '0':
          self.current_predictions_1[0] = ''
        if self.current_predictions_1[1] == '0' and self.current_predictions_1[0] is not '0':
          self.current_predictions_1[1] = ''
          
        query = 'http://localhost:8080/update_recipe?ingredient_ids1={}&ingredient_ids2={}&flying_pan=true&page_index=0&ingredient_name1={}&ingredient_name2={}&recognition_rate1={:.4f}&recognition_rate2={:.4f}'.format(
            self.current_predictions_1[0],
            self.current_predictions_1[1],
            self.current_instances[0],
            self.current_instances[1],
            recognition_rates[0],
            recognition_rates[1],
        )
        print('query', query)
        requests.get(query)
        t_query_1 = time.time()
        print('request time :', t_query_1 - t_query_0)
      else:
        print('not change')
        pass
      # send request when it detects gyoza
      if self.category_map[x.argmax()] == 'gyoza':
        print('detect gyoza')
        print('take a picture')
        print('*'*30 + ' request ' +'*'*30)
        t_query_0 = time.time()
        query = 'http://localhost:8080/update_recipe?ingredient_ids1=35&ingredient_ids2=42&flying_pan=true'
        print('query', query)
        requests.get(query)
        t_query_1 = time.time()
        print('request time :', t_query_1 - t_query_0)
      else:
        pass

class CookingThread(threading.Thread):
  def __init__(self,
               bbox2,
               # output_dir,
               checkpoint_file,
               category_map,
               # db_map,
               previous_predictions_2,
               status,
               bbox2_instance,):
    super(CookingThread, self).__init__()
    self.bbox2 = bbox2
    # self.output_dir = output_dir
    self.checkpoint_file = checkpoint_file
    self.category_map = category_map
    # self.db_map = db_map
    self.previous_predictions_2 = previous_predictions_2
    self.current_predictions_2 = 0
    self.status = status
    self.bbox2_instance = bbox2_instance
    
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
      bbox2 = self.bbox2[:,:,::-1]
      
      # evaluation
      log = str()
      bbox = bbox2
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

      # # output all class probabilities
      # for i in range(x.shape[1]):
      #   print(sys.stdout.write('%s : %s' % (self.category_map[i], x[0][i])))

      print('self.previous_predictions_2', self.previous_predictions_2)
      print('self.current_predictions_2', self.current_predictions_2)
      # print(self.previous_predictions_2 == self.current_predictions_2)

      # management cokking status
      self.current_predictions_2 = int(x.argmax())
      if self.previous_predictions_2 + 1 == self.current_predictions_2:
        self.status = self.current_predictions_2
        print('change')
        t_query_0 = time.time()
        query = 'http://localhost:8080/update_recipe?ingredient_ids1=35&ingredient_ids2=43&flying_pan=true'
        requests.get(query)
      else:
        pass
      print('current status: %s %s ' % (self.status, self.category_map[self.status]))
      
      #   t_query_1 = time.time()
      #   print('request time :', t_query_1 - t_query_0)
      # else:
      #   print('not change')
      #   pass


class CookwareThread(threading.Thread):
  def __init__(self,
               bbox1,
               # output_dir,
               checkpoint_file,
               category_map,
               bbox1_instances,
               current_instances,
               ingredient_current_instances,
               bbox1_category):
    super(CookwareThread, self).__init__()
    self.bbox1 = bbox1
    # self.output_dir = output_dir
    self.checkpoint_file = checkpoint_file
    self.category_map = category_map
    self.bbox1_instance = bbox1_category
    self.current_instances = []
    self.ingredient_current_instances = ingredient_current_instances
    self.bbox1_category = bbox1_category
    self.kettle_flag = False

  def run(self):
    print('category_map', self.category_map)
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
          num_classes=_COOKWARE_NUM_CLASSES,
          is_training=False,
      )
      
    vars = slim.get_variables_to_restore()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
      bbox1 = self.bbox1[:,:,::-1]
      
      # evaluation
      log = str()
      bbox = bbox1
      recognition_rates = []
      saver.restore(sess, self.checkpoint_file)
      x = end_points['Predictions'].eval(
          feed_dict={input: bbox}
      )
      # output top predicitons
      self.current_instances.append(self.category_map[x.argmax()])
      category_name = str(self.category_map[x.argmax()])
      print(sys.stdout.write('category_name %s' % category_name))
      probability = '{:.4f}'.format(x.max())
      self.bbox1_instance = str(category_name) + ' : ' + probability
      recognition_rates.append(x.max())
      print('self.bbox1_category', self.bbox1_category)
      print('self.category_map', self.category_map[x.argmax()])
      print(self.bbox1_category == self.category_map[x.argmax()])
      if self.bbox1_category == self.category_map[x.argmax()]:
        self.kettle_flag = True
      self.bbox1_category = self.category_map[x.argmax()]
      print('self.bbox1_category', self.bbox1_category)
      print(sys.stdout.write(
          'Top 1 prediction: %d %s %f'
          % (x.argmax(), self.category_map[x.argmax()], x.max())
      ))

      # output all class probabilities
      for i in range(x.shape[1]):
        print(sys.stdout.write('%s : %s' % (self.category_map[i], x[0][i])))

      self.current_instances.append(x.argmax())

      print('current_instances', self.current_instances)
      print('self.bbox1_instance', self.bbox1_instance)

      # when ingredient name1 and 2 is nothing, throw request which instance is kettle or not
      print('self.kettle_flag', self.kettle_flag)
      if self.kettle_flag == False:
        print('self.ingredient_current_instances', self.ingredient_current_instances)
        if self.ingredient_current_instances[0] == 'nothing' \
          and self.ingredient_current_instances[1] == 'nothing':
          if self.category_map[x.argmax()] == 'kettle':
            print('detect kettle')
            print('*'*15 + ' request ' +'*'*15)
            t_query_0 = time.time()
            query = 'http://localhost:8080/update_kettle?kettle_exist=true'
            print('query', query)
            requests.get(query)
            t_query_1 = time.time()
            print('request time :', t_query_1 - t_query_0)
          else:
            print('not kettle')
            t_query_0 = time.time()
            query = 'http://localhost:8080/update_kettle?kettle_exist=false'
            print('query', query)
            requests.get(query)
            t_query_1 = time.time()
            print('request time :', t_query_1 - t_query_0)
            pass
        else:
          pass


def main():
  now = datetime.now()
  today = now.strftime('%Y%m%d')
  
  t0 = time.time()

  # output_dir = os.path.join(_LOG_DIR, today)
  # if os.path.isdir(output_dir) is False:
  #   os.mkdir(output_dir)
   
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

  cookware_checkpoint_file = os.path.join(
      _COOKWARE_CHECKPOINT_PATH, _COOKWARE_CHECKPOINT_FILE
  )
  cookware_category_map = convert_label_files_to_dict(
      _COOKWARE_DATA_DIR, _COOKWARE_LABEL_DATA
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

  # start video capture
  count = 0
  previous_predictions_1 = []
  previous_predictions_2 = 0
  status = 0
  ingredient_current_instances = ['nothing', 'nothing']
  cookware_current_instances = []
  bbox1_category, bbox2_category, bbox3_category, bbox4_category = '','','',''

  bbox1_instance, bbox2_instance, bbox3_instance, bbox4_instance = 'bbox1', 'bbox2', 'bbox3', 'bbox4' 
  
  t1 = time.time()
  print('start ~ while :', t1 - t0)
  while(True):
    t3 = time.time()
    ret, frame = cap.read()
    share_margin = int(margin/2)
    text_margin = 10
    stings_space = 50

    # access category name for each thread class
    try:
      ingredient_current_instances = thread1.current_instances
      cookware_current_instances = thread3.current_instances
      # print('thread1.current_instances', thread1.current_instances)
      # print('type', type(thread1.current_instances))
      bbox1_instance = thread3.bbox1_instance
      bbox3_instance = thread1.bbox3_instance
      bbox4_instance = thread1.bbox4_instance
      bbox1_category = thread3.bbox1_category
    except UnboundLocalError:
      print('Unboundlocalerror')
      pass

    # # higobashi bbox
    # # bbox1(cookware)
    # cv2.rectangle(
    #     frame,
    #     ((center1_width-threshold-(share_margin)),
    #      (center_height-(threshold*3)-(share_margin))),
    #     ((center1_width+threshold+(share_margin)),
    #      (center_height-threshold-(share_margin))),
    #     (0,0,255),
    #     3
    # )
    # cv2.putText(
    #     frame,
    #     str(bbox1_instance),
    #     (center1_width-threshold, center_height-(threshold*3)-text_margin),
    #     cv2.FONT_HERSHEY_PLAIN,
    #     2,
    #     (255,0,0),
    #     3,
    #     cv2.LINE_AA
    # )
    # # bbox2(cooking)
    # cv2.rectangle(
    #     frame,
    #     ((center1_width-threshold-(share_margin)),
    #      (center_height-threshold-(share_margin))), # start coordinates
    #     ((center1_width+threshold+(share_margin)),
    #      (center_height+threshold+(share_margin))), # end coordinates
    #     (0,0,255),
    #     3
    # )
    # cv2.putText(
    #     frame,
    #     str(count),
    #     (center1_width-threshold, center_height+threshold+text_margin+stings_space),
    #     cv2.FONT_HERSHEY_PLAIN,
    #     2,
    #     (255,0,0),
    #     3,
    #     cv2.LINE_AA
    # )
    # # bbox3(ingredient1)
    # cv2.rectangle(
    #     frame,
    #     ((center2_width-threshold-(share_margin)),
    #      (center_height-threshold-(share_margin))), # start coordinates
    #     ((center2_width+threshold+(share_margin)),
    #      (center_height+threshold+(share_margin))), # end coordinates 
    #     (0,0,255),
    #     3
    # )
    # cv2.putText(
    #     frame,
    #     str(bbox3_instance),
    #     (center2_width-threshold, center_height-threshold-text_margin),
    #     cv2.FONT_HERSHEY_PLAIN,
    #     2,
    #     (255,0,0),
    #     3,
    #     cv2.LINE_AA
    # )
    # # bbox4(ingredient2)
    # cv2.rectangle(
    #     frame,
    #     ((center3_width-threshold-(share_margin)),
    #      (center_height-threshold-(share_margin))), # start coordinates
    #     ((center3_width+threshold+(share_margin)),
    #      (center_height+threshold+(share_margin))), # end coordinates
    #     (0,0,255),
    #     3
    # )
    # cv2.putText(
    #     frame,
    #     str(bbox4_instance),
    #     (center3_width-threshold, center_height-threshold-text_margin),
    #     cv2.FONT_HERSHEY_PLAIN,
    #     2,
    #     (255,0,0),
    #     3,
    #     cv2.LINE_AA
    # )

    # kusatsu bbox
    # bbox1(cookware)
    cv2.rectangle(
        frame,
        ((center1_width-threshold-(share_margin))-440,
         (center_height-threshold-(share_margin))+190), # start coordinates
        ((center1_width+threshold+(share_margin))-440,
         (center_height+threshold+(share_margin))+190), # end coordinates
        (0,0,255),
        3
    )
    cv2.putText(
        frame,
        str(bbox1_instance),
        (center1_width-threshold-440, (center_height+190)-(threshold)-(text_margin)),
        cv2.FONT_HERSHEY_PLAIN,
        1.5,
        (255,0,0),
        3,
        cv2.LINE_AA
    )
    # bbox2(cooking)
    cv2.rectangle(
        frame,
        ((center1_width-threshold-(share_margin))-440,
         (center_height-threshold-(share_margin))+190), # start coordinates
        ((center1_width+threshold+(share_margin))-440,
         (center_height+threshold+(share_margin))+190), # end coordinates
        (0,0,255),
        3
    )
    cv2.putText(
        frame,
        str(count),
        (center1_width-threshold-440, (center_height+190)+(threshold)+(text_margin*3)),
        cv2.FONT_HERSHEY_PLAIN,
        1.5,
        (255,0,0),
        3,
        cv2.LINE_AA
    )
    # bbox3(ingredient1)
    cv2.rectangle(
        frame,
        ((center2_width-threshold-(share_margin))-300,
         (center_height-threshold-(share_margin))+130), # start coordinates
        ((center2_width+threshold+(share_margin))-300,
         (center_height+threshold+(share_margin))+130), # end coordinates 
        (0,0,255),
        3
    )
    cv2.putText(
        frame,
        str(bbox3_instance),
        ((center2_width-300)-threshold, (center_height+130)-threshold-text_margin),
        cv2.FONT_HERSHEY_PLAIN,
        1.5,
        (255,0,0),
        3,
        cv2.LINE_AA
    )
    # bbox4(ingredient2)
    cv2.rectangle(
        frame,
        ((center3_width-threshold-(share_margin))-300,
         (center_height-threshold-(share_margin))+130), # start coordinates
        ((center3_width+threshold+(share_margin))-300,
         (center_height+threshold+(share_margin))+130), # end coordinates
        (0,0,255),
        3
    )
    cv2.putText(
        frame,
        str(bbox4_instance),
        ((center3_width-300)-threshold, (center_height+130)-threshold-text_margin),
        cv2.FONT_HERSHEY_PLAIN,
        1.5,
        (255,0,0),
        3,
        cv2.LINE_AA
    )

    cv2.imshow('frame', frame)
    # cv2.setMouseCallback('frame', print_coordinates)

    # ROI
    bbox1 = frame[center_height-threshold+190:center_height+threshold+190,
                  center1_width-threshold-440:center1_width+threshold-440]
    bbox2 = frame[center_height-threshold+190:center_height+threshold+190,
                  center1_width-threshold-440:center1_width+threshold-440]
    bbox3 = frame[center_height-threshold+130:center_height+threshold+130,
                  center2_width-threshold-300:center2_width+threshold-300]
    bbox4 = frame[center_height-threshold+130:center_height+threshold+130,
                  center3_width-threshold-300:center3_width+threshold-300]

    # # ROI dump
    # print('bbox1',
    #       (center_height-threshold*3+10, center_height-threshold-10),
    #       (center1_width-threshold, center1_width+threshold)
    # )
    # print('bbox2',
    #       (center_height-threshold, center_height+threshold),
    #       (center1_width-threshold,center1_width+threshold)
    # )
    # print('bbox3',
    #       (center_height-threshold, center_height+threshold),
    #       (center2_width-threshold, center2_width+threshold)
    # )
    # print('bbox4',
    #       (center_height-threshold, center_height+threshold),
    #       (center3_width-threshold, center3_width+threshold)
    # )

    print('kusatsu bbox1',
          (center_height-threshold*3+10+420,
           center_height-threshold-10+420),
          (center1_width-threshold-440,
           center1_width+threshold-440)
    )
    # print('kusatsu bbox2',
    #       (center_height-threshold-190,
    #        center_height+threshold+190),
    #       (center1_width-threshold-440,
    #        center1_width+threshold-440)
    # )
    # print('kusatsu bbox3',
    #       (center_height-threshold+130,
    #        center_height+threshold+130),
    #       (center2_width-threshold-300,
    #        center2_width+threshold-300)
    # )
    # print('kusatsu bbox4',
    #       (center_height-threshold+130,
    #        center_heihgt+threshold+130),
    #       (center3_width-threshold-300,
    #        center3_width+threshold-300)
    # )

    # # save image of bounding box
    # now = datetime.now()
    # seconds = now.strftime('%Y%m%d_%H%M%S') + '_' + str(now.microsecond)
    # cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox1.png', bbox1)
    # cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox2.png', bbox2)
    # cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox3.png', bbox3)
    # cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox4.png', bbox4)

    # # BGR t0 RGB
    # bbox1 = bbox1[:,:,::-1]
    # bbox2 = bbox2[:,:,::-1]
    # bbox3 = bbox3[:,:,::-1]

    if count % 15 == 1:
      thread1 = IngredientThread(
          bbox3,
          bbox4,
          # output_dir,
          ingredient_checkpoint_file,
          ingredient_category_map,
          db_map,
          previous_predictions_1,
          bbox3_instance,
          bbox4_instance,
          ingredient_current_instances,
          bbox3_category,
          bbox4_category,
        )
      thread1.start()
      previous_predictions_1 = thread1.current_predictions_1
      
    elif count % 15 == 6:
      thread2 = CookingThread(
          bbox2,
          # output_dir,
          cooking_checkpoint_file,
          cooking_category_map,
          # db_map,
          previous_predictions_2,
          status,
          bbox2_instance,
        )
      thread2.start()
      print('status', status)
      status = thread2.status
      
      previous_predictions_2 = thread2.status
      print('thread2.status', thread2.status)

      bbox2_instance = thread2.bbox2_instance

    elif count % 15 == 11:
      thread3 = CookwareThread(
          bbox1,
          # output_dir,
          cookware_checkpoint_file,
          cookware_category_map,
          bbox1_instance,
          cookware_current_instances,
          ingredient_current_instances,
          bbox1_category,
        )
      thread3.start()
      bbox1_category = thread3.bbox1_category
          
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
