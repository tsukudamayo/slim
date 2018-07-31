#!/bin/bash

DATASET_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_256_manually_select
CHECKPOINT_FILE=/media/panasonic/644E9C944E9C611A/tmp/model/20180730_food_5class_alexnet/model.ckpt-50000

python eval_image_classifier.py --alsologstderr --batch_size=2 --checkpoint_path=${CHECKPOINT_FILE} --dataset_dir=${DATASET_DIR} --dataset_name=food --dataset_split_name=validation --model_name=alexnet_v2  2>&1 | tee stderr.log


