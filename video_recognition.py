from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time

import numpy as np
import cv2
import tensorflow as tf

from nets import mobilenet_v1

slim = tf.contrib.slim

tf.app.flags.DEFINE_string(
    'checkpoint_path', '/media/panasonic/644E9C944E9C611A/tmp/model/20180726_food_2class_mobilenet_v1_finetune/model.ckpt-1814',
    'The directory where the model was written to or an absolute path to a '
    'checkpoint file.')

tf.app.flags.DEFINE_string(
    'model_name', 'mobilenet_v1', 'The name of the architecture to evaluate.')

tf.app.flags.DEFINE_integer(
    'eval_image_size', 224, 'Eval image size')

FLAGS = tf.app.flags.FLAGS


_MODEL_DIR = '/media/panasonic/644E9C944E9C611A/tmp/model/20180726_food_2class_mobilenet_v1_finetune'
_CHECKPOINT_PATH = '/media/panasonic/644E9C944E9C611A/tmp/model/20180726_food_2class_mobilenet_v1_finetune'
_META_FILE = 'model.ckpt-1814.meta'
_CHECKPOINT_FILE = 'model.ckpt-1814'
_IMAGE_DIR = 'image'

category_map = {
    0: 'broccoli',
    1: 'tomato',
}


def main():
    t0 = time.time()

    #--------------#
    # define model #
    #--------------#
    checkpoint_file = os.path.join(_CHECKPOINT_PATH, _CHECKPOINT_FILE)

    tf.reset_default_graph()
    
    # file_input = tf.placeholder(tf.string, ())
    # image = tf.image.decode_png(tf.read_file(file_input))
    input = tf.placeholder('float', [None,None,3])
    images = tf.expand_dims(input, 0)
    images = tf.cast(images, tf.float32)/128 - 1
    images.set_shape((None,None,None,3))
    images = tf.image.resize_images(images,(224,224))

    with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
        logits, end_points = mobilenet_v1.mobilenet_v1(
            images,
            num_classes=2,
            is_training=False,
        )

    # ema = tf.train.ExponentialMovingAverage(0.999)
    # vars = ema.variables_to_restore()
    vars = slim.get_variables_to_restore()
    saver = tf.train.Saver()
    
    #-----------------------------#
    # videocapture and prediction #
    #-----------------------------#
    with tf.Session() as sess:
        cap = cv2.VideoCapture(0)
        
        while(True):
            ret, frame = cap.read()
            cv2.rectangle(frame,
                          ((320-30),(240-30)),
                          ((320+30),(240+30)),
                          (0,0,255),
                          3)
            cv2.imshow('frame', frame)
            bbox = frame[(320-30):(320+30), (240-30):(240+30)]
            # print('bbox', bbox)
            bbox = cv2.resize(bbox,(224,224))
            # print('bbox/resize', bbox)
            bbox = np.expand_dims(bbox, 0)
            
            saver.restore(sess, checkpoint_file)
            x = end_points['Predictions'].eval(
                feed_dict={images: bbox}
            )
            print(sys.stdout.write(
                'Top 1 prediction: %d %s %f'
                % (x.argmax(), category_map[x.argmax()], x.max())
            ))
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
