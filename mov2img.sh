#!/bin/bash

_TODAY=$(date +'%Y%m%d')
echo $_TODAY

_MOV_DIR='/media/panasonic/644E9C944E9C611A/tmp/data/mov/ingradient/tomato/'${_TODAY}
_TARGET_DIR='/media/panasonic/644E9C944E9C611A/tmp/data/img/food_kurashiru_224_'${_TODAY}

echo ${_MOV_DIR}
echo ${_TARGET_DIR}
mkdir ${_TARGET_DIR}

count=0
for f in `ls ${_MOV_DIR} | grep webm`
do
    echo $count
    echo $f
    dir_name=$(echo $count | xargs -P1 printf '%06d\n')
    echo $dir_name
    mkdir ${_TARGET_DIR}'/'$dir_name

    cd ${_TARGET_DIR}'/'$dir_name
    ffmpeg -i ${_MOV_DIR}'/'$f -s 224x224 %06d.png
    
    count=$((count+1))
done
