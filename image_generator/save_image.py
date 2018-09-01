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


def main():
    now = datetime.now()
    today = now.strftime('%Y%m%d')

    t0 = time.time()

    output_dir = os.path.join(_LOG_DIR, today)
    if os.path.isdir(output_dir) is False:
        os.mkdir(output_dir)

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
        cv2.imwrite(fname, bbox)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
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
