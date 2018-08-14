#!/bin/bash

DATASET_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_256_manually_select_20180814_ep_tm_cu
CHECKPOINT_FILE=/media/panasonic/644E9C944E9C611A/tmp/model/20180814_food_256_manually_select_ep_tm_cu_mobilenet_v1_1_224_finetune/model.ckpt-20000

python eval_image_classifier.py --alsologstderr --batch_size=2 --checkpoint_path=${CHECKPOINT_FILE} --dataset_dir=${DATASET_DIR} --dataset_name=food --dataset_split_name=validation --model_name=mobilenet_v1 2>&1 | tee stderr.log
