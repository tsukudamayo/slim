#!/bin/bash

DATA_DIR=~/tmp/data/flowers

mkdir -p ${DATA_DIR}

python download_and_convert_data.py --dataset_name=flowers --dataset_dir=${DATA_DIR}
