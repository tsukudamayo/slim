#!/bin/bash

DATA_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/cooking_kurashiru_20181016_x_10
mkdir -p ${DATA_DIR}

python download_and_convert_data.py --dataset_name=food --dataset_dir=${DATA_DIR}
