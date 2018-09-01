#!/bin/bash

DATA_DIR=/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_dossari_20180816_validation
mkdir -p ${DATA_DIR}

python download_and_convert_data.py --dataset_name=food --dataset_dir=${DATA_DIR}
