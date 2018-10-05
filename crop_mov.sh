#!/bin/bash

_MOV_DIR=$1
_TARGET_DIR=$2

echo ${_MOV_DIR}
echo ${_TARGET_DIR}
mkdir ${_TARGET_DIR}

count=0
for f in `ls ${_MOV_DIR} | grep mp4`
do
    echo $count
    echo $f
    echo ${_MOV_DIR}$f
    
    mkdir ${_TARGET_DIR}

    cd ${_TARGET_DIR}
    echo $f
    ffmpeg -i ${_MOV_DIR}$f -vf crop=224:224:860:500  $f

    count=$((count+1))
    
done
