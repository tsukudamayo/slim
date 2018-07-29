#!/bin/bash

DATASET_DIR=~/tmp/data/flowers
TRAIN_DIR=~/tmp/model/flowers
CHECKPOINT_FILE=~/tmp/pretrained/inception_v3.ckpt

mkdir -p ${TRAIN_DIR}

python train_image_classifier.py --train_dir=${TRAIN_DIR} --dataset_name=flowers --dataset_split_name=train --dataset_dir=${DATASET_DIR} --model_name=inception_v3 --checkpoint_path=${CHECKPOINT_FILE} --checkpoint_exclude_scopes=InceptionV3/Logits,InceptionV3/AuxLogits --trainable_scopes=InceptionV3/Logits,InceptionV3/AuxLogits
