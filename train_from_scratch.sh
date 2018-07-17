#!/bin/bash

DATASET_DIR=~/tmp/data/flowers
TRAIN_DIR=~/tmp/model/flowers

mkdir -p ${TRAIN_DIR}

python train_image_classifier.py --train_dir=${TRAIN_DIR} --dataset_name=flowers --dataset_split_name=train --dataset_dir=${DATASET_DIR} --model_name=inception_v3
