from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time
from datetime import datetime

import numpy as np
import cv2
import tensorflow as tf

#-----------#
# constants #
#-----------#
_LOG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/log'
_MOV_DIR = '/media/panasonic/644E9C944E9C611A/tmp/log/mov'


def main():
    now = datetime.now()
    today = now.strftime('%Y%m%d')

    t0 = time.time()

    output_dir = os.path.join(_LOG_DIR, today)
    if os.path.isdir(_LOG_DIR) is False:
        os.mkdir(_LOG_DIR)
    if os.path.isdir(_LOG_DIR) is False:
        os.mkdir(_MOV_DIR)
    if os.path.isdir(output_dir) is False:
        os.mkdir(output_dir)

    #------------------------------------------------#
    # define the codec and create VideoWriter object #
    #------------------------------------------------#
    movie_path = os.path.join(
        _MOV_DIR, str(now.strftime('%Y%m%d_%H%M%S')) + '.avi'
    )
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(movie_path,
                            fourcc,
                            20.0,
                            (1920, 1080))

    #-----------------------------#
    # videocapture and prediction #
    #-----------------------------#
    width = 1920
    height = 1080

    threshold = int(224 / 2) # default (224 / 2)
    margin = 10              # not to capture bounding box

    center_width = int(width / 2)
    center_height = int(height / 2)

    cap = cv2.VideoCapture(0)
    
    # camera propety(1920x1080)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    
    while(True):
        ret, frame = cap.read()
        if ret == True:
          cv2.rectangle(
              frame,
              ((center_width-threshold-margin),(center_height-threshold-margin)),
              ((center_width+threshold+margin),(center_height+threshold+margin)),
              (0,0,255),
              3
          )
          cv2.imshow('frame', frame)
          bbox = frame[center_height-threshold:center_height+threshold,
                       center_width-threshold:center_width+threshold]
          bbox = cv2.resize(bbox,(224,224))
          now = datetime.now()
          seconds = now.strftime('%Y%m%d_%H%M%S')
          micro_seconds = now.microsecond
          fname = os.path.join(output_dir, seconds) + '_' + str(micro_seconds) + '.png'
          video.write(bbox)
          # cv2.imwrite(fname, bbox)
          if cv2.waitKey(1) & 0xFF == ord('q'):
              break
    cap.release()
    video.release()
    cv2.destroyAllWindows()
            
    #     bbox = frame[center_height-threshold:center_height+threshold,
    #                  center_width-threshold:center_width+threshold]
    #     bbox = cv2.resize(bbox,(224,224))
    #     now = datetime.now()
    #     seconds = now.strftime('%Y%m%d_%H%M%S')
    #     cv2.imwrite(os.path.join(output_dir, seconds) + '.png', bbox)
        
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
        
    #     cap.release()
    #     cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
