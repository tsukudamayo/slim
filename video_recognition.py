from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import math

import numpy as np
import cv2
import tensorflow as tf




def main():

    cap = cv2.VideoCapture(0)
    
    while(True):
        # capture frame-by-frame
        ret, frame = cap.read()
    
        cv2.rectangle(frame,(540,300),(764,524),(0,0,255),3)
    
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
