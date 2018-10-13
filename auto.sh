#!/bin/bash

python image_generator/image_data_generator.py
./convert_image.sh 

./train_finetuning.sh
# ./train_finetuning_1.sh 


# cd ../tm_object_detection_api/
# ./train_finetuning.sh
