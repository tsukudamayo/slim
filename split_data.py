import os,sys
import shutil

import numpy as np


_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/food_dossari_20180815_ep_camera2'
_DST_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/food_dossari_20180815_cu_ep_tm_camera2'
_CATEGORY = 'eggplant'
_TEST_SIZE = 0.1

# random seed
np.random.seed(0)


def main():
    # all file path
    all_data_files = np.array(
        [os.path.join(_DATA_DIR, f) for f in os.listdir(_DATA_DIR)]
    )
    
    # shuffle data
    shuffle_idx = np.random.permutation(len(all_data_files))
    print('shuffle_idx', shuffle_idx)
    shuffle_data = all_data_files[shuffle_idx]
    
    # split train data and test data
    training_size = int(len(all_data_files) * (1 - _TEST_SIZE))
    train_data = shuffle_data[:training_size]
    test_data = shuffle_data[training_size:]
    print('train data\n', len(train_data))
    print('test data\n', len(test_data))
    
    # define filepath
    train_dir = os.path.join(_DST_DIR, 'train')
    test_dir = os.path.join(_DST_DIR, 'validation')
    category_train = os.path.join(train_dir, _CATEGORY)
    category_test = os.path.join(test_dir, _CATEGORY)
    make_directories = [
        _DST_DIR,
        train_dir,
        test_dir,
        category_train,
        category_test,
    ]
    # make directories 
    [os.mkdir(directory)
         for directory in make_directories
         if os.path.isdir(directory) is False]

    # copy train data and test data
    for f in train_data:
        copy_file = os.path.join(category_train, os.path.basename(f))
        shutil.copy2(f, copy_file)    
    for f in test_data:
        copy_file = os.path.join(category_test, os.path.basename(f))
        shutil.copy2(f, copy_file)


if __name__ == '__main__':
    main()
