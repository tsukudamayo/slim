import os,sys
import shutil

import numpy as np


_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/food_dossari_20180816_validation_cu'
_DST_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/img/food_dossari_20180816_validation'
_CATEGORY = 'cucumber'
_NUMBER_OF_SAMPLING = 100
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
    sampling_data = shuffle_data[:_NUMBER_OF_SAMPLING]
    print('sampling data\n', len(sampling_data))
    
    # define filepath
    sampling_dir = os.path.join(_DST_DIR, _CATEGORY)

    # make directories
    if os.path.exists(_DATA_DIR) is False:
        os.mkdir(sampling_dir)
    if os.path.exists(sampling_dir) is False:
        os.mkdir(sampling_dir)

    # copy train data and test data
    for f in sampling_data:
        copy_file = os.path.join(sampling_dir, os.path.basename(f))
        shutil.copy2(f, copy_file)


if __name__ == '__main__':
    main()


