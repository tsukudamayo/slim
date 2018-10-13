#!/bin/bash

DATASET_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/cookware_google_search_224_20181013_x_10
TRAIN_DIR=/media/panasonic/644E9C944E9C611A/tmp/model/20181013_cookware_google_search_224_18class_x_10_mobilenet_v1_1_224_finetune
CHECKPOINT_PATH=/media/panasonic/644E9C944E9C611A/tmp/pretrained/mobilenet_v1_1_224/mobilenet_v1_1.0_224.ckpt

mkdir -p ${TRAIN_DIR}

python train_image_classifier.py \
       --train_dir=${TRAIN_DIR} \
       --dataset_name=food \
       --dataset_split_name=train \
       --dataset_dir=${DATASET_DIR} \
       --model_name=mobilenet_v1 \
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
       --max_number_of_steps=20000 \
       --train_image_size=224 \
       --checkpoint_path=${CHECKPOINT_PATH} \
       --checkpoint_exclude_scope=MobilenetV1/Logits \
       --trainable_scopes=MobilenetV1/Logits,
