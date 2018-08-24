#!/bin/bash

DATASET_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_224_keep_aspect_ratio_20180809_3class
CHECKPOINT_FILE=/media/panasonic/644E9C944E9C611A/tmp/model/20180809_food_224_keep_aspect_ratio_3class_x10_share_range_0_mobilenet_v1_1_224_finetune/model.ckpt-20000

python eval_image_classifier.py --alsologstderr --batch_size=25 --checkpoint_path=${CHECKPOINT_FILE} --dataset_dir=${DATASET_DIR} --dataset_name=food --dataset_split_name=validation --model_name=mobilenet_v1 2>&1 | tee stderr.log
