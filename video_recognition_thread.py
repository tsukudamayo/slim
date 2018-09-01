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

# #TODO(FLAGS)
# tf.app.flags.DEFINE_string(
#     'checkpoint_path', '/media/panasonic/644E9C944E9C611A/tmp/model/20180726_food_2class_mobilenet_v1_finetune/model.ckpt-1814',
#     'The directory where the model was written to or an absolute path to a '
#     'checkpoint file.')

# tf.app.flags.DEFINE_string(
#     'model_name', 'mobilenet_v1', 'The name of the architecture to evaluate.')

# tf.app.flags.DEFINE_integer(
#     'eval_image_size', 224, 'Eval image size')

FLAGS = tf.app.flags.FLAGS

#-----------#
# constants #
#-----------#
_URL = 'http://localhost:8080/update_recipe'
_NUM_CLASSES = 3
_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_224_dossari_20180815_cu_ep_tm_x10'
_LABEL_DATA = 'labels.txt'
_DB_DATA = 'labels_db.txt'
_CHECKPOINT_PATH = '/media/panasonic/644E9C944E9C611A/tmp/model/20180815_food_dossari_cu_ep_tm_x10_mobilenet_v1_1_224_finetune'
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


class detection_thread(threading.Thread):
  def __init__(self,
               bbox1,
               bbox2,
               output_dir,
               checkpoint_file,
               category_map,
               db_map,
               previous_predictions,):
    super(detection_thread, self).__init__()
    self.bbox1 = bbox1
    self.bbox2 = bbox2
    self.output_dir = output_dir
    self.checkpoint_file = checkpoint_file
    self.category_map = category_map
    self.db_map = db_map
    self.previous_predictions = previous_predictions
    self.current_predictions = []
    
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
          num_classes=_NUM_CLASSES,
          is_training=False,
      )
      
    vars = slim.get_variables_to_restore()
    saver = tf.train.Saver()
    
    with tf.Session() as sess:
      bbox1 = self.bbox1 / 128 - 1
      bbox2 = self.bbox2 / 128 - 1
      bbox1 = np.expand_dims(bbox1, 0)
      bbox2 = np.expand_dims(bbox2, 0)
      
      # evaluation
      log = str()
      all_bbox = [bbox1, bbox2]
      bbox_names = ['left', 'right']
      for bbox, bbox_name in zip(all_bbox, bbox_names):
        saver.restore(sess, self.checkpoint_file)
        x = end_points['Predictions'].eval(
            feed_dict={images: bbox}
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

        self.current_predictions.append(pred_id)

        # send GET request if prediction is changed
      # send_get_request(_URL, 'gradient', self.category_map[x.argmax()])
      # print('send GET')
      # print('time :', datetime.now().strftime('%Y%m%d:%H%M%S'))
      # prediction_category = x.argmax()
      # requests.get('http://localhost:8080/update_recipe?ingredient_ids=42,46&ingredient_ids2=43,617&flying_pan=true&page_index=0')
      print('self.previous_predictions', self.previous_predictions)
      print('self.current_predictions', self.current_predictions)
      print(self.previous_predictions == self.current_predictions)
      if self.previous_predictions != self.current_predictions:
        print('change')
        t_query_0 = time.time()
        query = 'http://localhost:8080/update_recipe?ingredient_ids1={}&ingredient_ids2={}&flying_pan=true'.format(
            self.current_predictions[0],
            self.current_predictions[1],
        )
        # # query = 'http://localhost:3000?ingredient_ids={0}&ingredient_ids2={1}&flying_pan=true'.format(
        # #     current_predictions[0],
        # #     current_predictions[1],
        # # )
        requests.get(query)
        t_query_1 = time.time()
        print('request time :', t_query_1 - t_query_0)
      else:
        print('not change')
        pass


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
  db_map = convert_label_files_to_dict(_DATA_DIR, _DB_DATA)

  #-----------------------------#
  # videocapture and prediction #
  #-----------------------------#
  width = 1920
  height = 1080

  # define ROI
  threshold = int(224 / 2)                         # default (224 / 2)
  margin = 10                                      # not to capture bounding box

  center = int(width * 5.5/10)
  center1_width = int(center - threshold) - margin # ROI1 center x
  center2_width = int(center + threshold) + margin # ROI2 center x
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
  previous_predictions = []
  t1 = time.time()
  print('start ~ while :', t1 - t0)
  while(True):
    t3 = time.time()
    ret, frame = cap.read()
    
    cv2.rectangle(
        frame,
        ((center1_width-threshold-margin),(center_height-threshold-margin)),
        ((center1_width+threshold+margin),(center_height+threshold+margin)),
        (0,0,255),
        3
    )
    cv2.rectangle(
        frame,
        ((center2_width-threshold-margin),(center_height-threshold-margin)),
        ((center2_width+threshold+margin),(center_height+threshold+margin)),
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
    
    bbox1 = cv2.resize(bbox1,(224,224))
    bbox2 = cv2.resize(bbox2,(224,224))
    
    # save image of bounding box
    now = datetime.now()
    seconds = now.strftime('%Y%m%d_%H%M%S') + '_' + str(now.microsecond)
    cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox1.png', bbox1)
    cv2.imwrite(os.path.join(output_dir, seconds) + '_bbox2.png', bbox2)

    if count % 5 == 0:
      thread = detection_thread(
          bbox1,
          bbox2,
          output_dir,
          checkpoint_file,
          category_map,
          db_map,
          previous_predictions,
        )
      thread.start()
      previous_predictions = thread.current_predictions
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
