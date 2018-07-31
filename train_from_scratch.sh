#!/bin/bash

DATASET_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_256_manually_select
TRAIN_DIR=/media/panasonic/644E9C944E9C611A/tmp/model/20180730_food_5class_alexnet

mkdir -p ${TRAIN_DIR}

python train_image_classifier.py \
       --train_dir=${TRAIN_DIR} \
       --dataset_name=food \
       --dataset_split_name=train \
       --dataset_dir=${DATASET_DIR} \
       --model_name=alexnet_v2 \
       --batch_size=32 \
       --optimizer=rmsprop \
       --rmsprop_decay=0.9 \
       --opt_epsilon=1.0 \
       --learning_rete=0.01 \
       --learning_rate_decay_factor=0.1 \
       --momentum=0.9 \
       --num_epocs_per_decay=2.0 \
       --log_every_n_steps=10 \
       --save_summaries_secs=300 \
       --save_interval_secs=300 \
       --max_number_of_steps=50000 \
       --train_image_size=224 \
       # --checkpoint_path=${CHECKPOINT_PATH} \
       # --checkpoint_exclude_scope=MobilenetV1/Logits \
       # --trainable_scopes=MobilenetV1/Logits,
