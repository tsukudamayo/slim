import os
import math
import time

import numpy as np
import tensorflow as tf
from tensorflow.contrib.tensorboard.plugins import projector

from nets import mobilenet_v1

slim = tf.contrib.slim

_NUM_CLASSES = 3
_LOG_DIR = '/media/panasonic/644E9C944E9C611A/tmp/projector/20180815_food_dossari_cu_ep_tm_x10_mobilenet_v1_1_224_finetune'
_CHECKPOINT_PATH = '/media/panasonic/644E9C944E9C611A/tmp/model/20180815_food_dossari_cu_ep_tm_x10_mobilenet_v1_1_224_finetune'
_CHECKPOINT_FILE = 'model.ckpt-20000'
_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/food_dossari_20180806_x10/validation'
_META_FILE = 'metadata.tsv'


def inquiry_filelist(data_dir):
    file_list = []
    for root, dirs, files in sorted(os.walk(data_dir)):
        for f in files:
            filepath = os.path.join(root, f)
            file_list.append(filepath)

    return file_list


def convert_labels_files_to_dict(data_dir, label_file):
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
        value = key_value[1].split()[0]
        category_map[key] = value

    return category_map


def main():
    t0 = time.time()

    output_dir = _LOG_DIR
    if os.path.isdir(output_dir) is False:
        os.mkdir(output_dir)

    checkpoint_file = os.path.join(_CHECKPOINT_PATH, _CHECKPOINT_FILE)
    category_map = convert_labels_files_to_dict(_DATA_DIR, _LABEL_DATA)

    eval_graph = tf.Graph()
    with eval_graph.as_default():

        file_input = tf.read_file(fname)
        input = tf.image.decode_png(tf.read_file(file_input), channels=3)
        images = tf.expand_dims(input, 0)
        images = tf.cast(images, tf.float32) / 128 - 1
        images.set_shape((None, None, None, 3))
        
        labels = tf.placeholder(tf.float32, [1, _NUM_CLASSES])

        with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
            logits, end_points = mobilenet_v1.mobilenet_v1(
                images,
                num_classes=_NUM_CLASSES,
                is_training=False,
            )

        vars = slim.get_variables_to_restore()
        saver = tf.train.Saver()

        filelist = inquiry_filelist(_DATA_DIR)
        
        with tf.Session(): as sess:
            saver.restore(sess, checkpoint_file)
            x = end_points['Conv2d_13_pointwise'].eval(
                feed_dict{

            outputs, files, eval_image = [], [], []
            
        
            

    


if __name__ == '__main__':
    main()
