from __future__ import print_function

import argparse

import tensorflow as tf

from nets import mobilenet_v1
from datasets import imagenet


slim = tf.contrib.slim


category_map = {
    0: 'brocolli',
    1: 'tomato',
}

label_map = imagenet.create_readable_names_for_imagenet_labels()


def main(checkpoint_file, eval_image):
    tf.reset_default_graph()

    file_input = tf.placeholder(tf.string, ())

    image = tf.image.decode_jpeg(tf.read_file(file_input))
    images = tf.expand_dims(image, 0)
    images = tf.cast(images, tf.float32)/128 - 1
    images.set_shape((None, None, None, 3))
    images = tf.image.resize_images(images, (224,224))

    with tf.contrib.slim.arg_scope(mobilenet_v1.mobilenet_v1_arg_scope()):
        logits, end_points = mobilenet_v1.mobilenet_v1(
            images,
            num_classes=6,
            is_training=False,
        )

    # ema = tf.train.ExponentialMovingAverage(0.999)
    # vars = ema.variables_to_restore()
    vars = slim.get_variables_to_restore()
    saver = tf.train.Saver(vars)

    with tf.Session() as sess:
        saver.restore(sess, checkpoint_file)
        x = end_points['Predictions'].eval(
            feed_dict={file_input: eval_image}
        )

    print('Top 1 prediction: ', x.argmax(), category_map[x.argmax()], x.max())  



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='evaluate image once by tensorflow model'
    )
    parser.add_argument('--checkpoint_file',
                        dest='checkpoint_file',
                        type=str,
                        default=None,
                        help='please enter the checkpoint file(.ckpt) path')
    parser.add_argument('--eval_image',
                        dest='eval_image',
                        type=str,
                        default=None,
                        help='please enter the image file name')
    argv = parser.parse_args()

    # main
    main(argv.checkpoint_file, argv.eval_image)
