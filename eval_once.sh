#!/bin/bash

DATASET_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_256_manually_select
CHECKPOINT_PATH=/media/panasonic/644E9C944E9C611A/tmp/model/20180726_food_5class_mobilenet_v1_finetune/model.ckpt-20135

python eval_image_classifier.py \
       --alsologstderr \
       --checkpoint_path=${CHECKPOINT_PATH} \
       --dataset_dir=${DATASET_DIR} \
       --dataset_name=food \
       --dataset_split_name=validation \
       --model_name=mobilenet_v1 \
       --batch_size=2 1 2>&1 | tee stderr.log
