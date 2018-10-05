#!/bin/bash

DATASET_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_google_search_224_20180927_x_10
CHECKPOINT_FILE=/media/panasonic/644E9C944E9C611A/tmp/model/20180927_food_google_search_224_17class_x_10_mobilenet_v1_1_224_finetune/model.ckpt-20000

python eval_image_classifier.py --alsologstderr --batch_size=2 --checkpoint_path=${CHECKPOINT_FILE} --dataset_dir=${DATASET_DIR} --dataset_name=food --dataset_split_name=validation --model_name=mobilenet_v1 2>&1 | tee stderr.log
