import os,sys
import shutil
import argparse
from distutils.util import strtobool

import numpy as np


# random seed
np.random.seed(0)


# TODO test
def copy_not_to_dupricate_fname(target_dir, file_path, filename_duplicate):
    """join directory name and file name for not to duplicate copy file name"""
    dir_name = os.path.basename(os.path.dirname(file_path))
    fname = os.path.basename(os.path.basename(file_path))
    if filename_duplicate == 1:
        # for not to dupricate filename when copy file of other directories
        fname_not_to_duplicate = dir_name + '_' + fname
        copy_file = os.path.join(target_dir, fname_not_to_duplicate)
    else:
        # copy file normally
        copy_file = os.path.join(target_dir, fname)
    shutil.copy2(file_path, copy_file)

    return


def main(data_dir, dst_dir,
         category, number_of_sampling,
         split_train_or_test, filename_duplicate):
    #-------------------#
    # get all file path #
    #-------------------#
    all_data_files = np.array([])
    for root, dirs, files in sorted(os.walk(data_dir)):
        for f in files:
            filepath = os.path.join(root, f)
            all_data_files = np.append(all_data_files, filepath)

    print('all_data_files', all_data_files)

    #--------------#
    # shuffle data #
    #--------------#
    shuffle_idx = np.random.permutation(len(all_data_files))
    print('shuffle_idx', shuffle_idx)
    shuffle_data = all_data_files[shuffle_idx]

    print('split_train_or_test', split_train_or_test)
    # split train data and test data
    if split_train_or_test == 1: # split_train_or_test is True
        training_data = shuffle_data[:number_of_sampling]
        validation_data = shuffle_data[number_of_sampling:]
        print('validation_data\n', len(validation_data))
        print('training_data \n', len(training_data))
    # do not split data
    elif split_train_or_test == 0: # split_train_or_test is False
        sampling_data = shuffle_data[:number_of_sampling]
        print('sampling data\n', len(sampling_data))

    #-------------------------#
    # make target directories #
    #-------------------------#
    if os.path.exists(data_dir) is False:
        os.mkdir(data_dir)
    if os.path.exists(dst_dir) is False:
        os.mkdir(dst_dir)

    # TODO test
    print('split_train_or_test', split_train_or_test)
    #------------------------------------------------------------#
    # copy train data and test data or just random sampling data #
    #------------------------------------------------------------#
    if split_train_or_test == 1: # split_train_or_test is True
        validation_dir = os.path.join(dst_dir, 'validation')
        if os.path.exists(validation_dir) is False:
            os.mkdir(validation_dir)
        validation_dir = os.path.join(validation_dir, category)
        if os.path.exists(validation_dir) is False:
            os.mkdir(validation_dir)
        for f in validation_data:
            copy_not_to_dupricate_fname(validation_dir, f, filename_duplicate)

        training_dir = os.path.join(dst_dir, 'train')
        if os.path.exists(training_dir) is False:
            os.mkdir(training_dir)
        training_dir = os.path.join(training_dir, category)
        if os.path.exists(training_dir) is False:
            os.mkdir(training_dir)
        for f in training_data:
            copy_not_to_dupricate_fname(training_dir, f, filename_duplicate)
            
    elif split_train_or_test == 0: # split_train_or_test is False
        sampling_dir = os.path.join(dst_dir, category)
        if os.path.exists(sampling_dir) is False:
            os.mkdir(sampling_dir)
        for f in sampling_data:
            copy_not_to_dupricate_fname(sampling_dir, f, filename_duplicate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',
                        dest='data_dir',
                        type=str,
                        default=None,
                        help='enter the filepath of parent directory'
                             'that you want to do sampling')
    parser.add_argument('--dst_dir',
                        dest='dst_dir',
                        type=str,
                        default=None,
                        help='enter the filepath that you want to output sample')
    parser.add_argument('--category',
                        dest='category',
                        type=str,
                        default=None,
                        help='enter the filepath that you want to do sampling')
    parser.add_argument('--number_of_sampling',
                        dest='number_of_sampling',
                        type=int,
                        default=0,
                        help='enter the number that you want to do sampling')
    parser.add_argument('--split_train_or_test',
                        dest='split_train_or_test',
                        type=strtobool,
                        default=False,
                        help='if True, generate evaluation data'
                             'specified "--number_of_sampling" numbers'
                             'and remaining data is training data.'
                             'if False, generate sampling data'
                             'specified "--number_of_sampling" numbers'
                             'from all data')
    parser.add_argument('--filename_duplicate',
                        dest='filename_duplicate',
                        type=strtobool,
                        default=False,
                        help='if True join directory name and filename'
                             'not to duplicate copy filename'
                             'if False, just copy file')
    argv = parser.parse_args()
    
    main(argv.data_dir, argv.dst_dir,
         argv.category, argv.number_of_sampling,
         argv.split_train_or_test, argv.filename_duplicate)
