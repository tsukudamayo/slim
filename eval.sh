#!/bin/bash

DATASET_DIR=~/tmp/data/flowers
CHECKPOINT_FILE=~/tmp/model/flowers/model.ckpt-656

python eval_image_classifier.py --alsologstderr --checkpoint_path=${CHECKPOINT_FILE} --dataset_dir=${DATASET_DIR} --dataset_name=flowers --dataset_split_name=validation --model_name=inception_v3  2>&1 | tee stderr.log


