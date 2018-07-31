import gc
from datetime import datetime

import numpy as np
import pandas as pd


def parse_tensorflow_logging(strings):
    """
    input : one line in the tensorflow log
    output : convert log into python's list
    - example
        - before
        2018-07-20 10:09:47.553780: I tensorflow/core/kernels/logging_ops.cc:79] predictions[2 2 2 2 4 0 4 0 2 1 3 0 3 1 3 4 3 4 3 p4 3 4 3 0 4 4 1 2 4 4 4 4]
        - after
        ['2', '2', '2', '2', '4', '0', '4', '0', '2', '1', '3', '0', '3', '1', '3', '4', '3', '4', '3', '4', '3', '4', '3', '0', '4', '4', '1', '2', '4', '4', '4', '4']
    """
    return np.array(strings.split('[')[1].split(']')[0].split())


def parse_tensorflow_logging_2d(strings):
    strings = strings.split('][')
    array_2d = []
    for idx, row in enumerate(strings):
        if idx == 0:
            row = str(row).split('[[')[1]
        elif idx == len(strings):
            row = str(row).split(']]')[0]
        row = str(row).split()
        array_2d.append(row)

    return np.array(array_2d)
        

# TODO
def duplicate_detection(strings):
    return


def dump_result(predictions, labels, filenames, categorynames, probabilities):
    now = datetime.now()
    date = now.strftime('%Y%m%d')
    
    df = pd.DataFrame({
        'prediction': predictions,
        'label': labels,
        'filename': filenames,
        'categorynames': categorynames,
    })

    probabilities = np.array(probabilities)
    df_prob = pd.DataFrame(probabilities)
    gen_prob_columns = ['prob_' + str(i) for i in range(probabilities.shape[1])]
    df_prob.columns = gen_prob_columns


    df = pd.concat([df, df_prob], axis=1)
    del now, df_prob
    gc.collect()
    
    df.to_csv(str(date) + '_result.csv')


def main():
    with open('stderr.log') as f:
        lines = f.readlines()
    
    predictions, labels, filenames, categorynames, probabilities = [], [], [], [], []
    for line in lines:
        print(line)
        if line.find('predictions[') >= 0:
            line = parse_tensorflow_logging(line)
            predictions.extend(line)
        elif line.find('labels[') >= 0:
            line = parse_tensorflow_logging(line)
            labels.extend(line)
        elif line.find('filenames[') >= 0:
            line = parse_tensorflow_logging(line)
            filenames.extend(line)
        elif line.find('categorynames[') >= 0:
            line = parse_tensorflow_logging(line)
            categorynames.extend(line)
        elif line.find('probabilities[') >= 0:
            line = parse_tensorflow_logging_2d(line)
            probabilities.extend(line)
        else:
            pass

    dump_result(predictions, labels, filenames, categorynames, probabilities)

    # **************** debug print ****************
    print('prediction\n', predictions)
    print('labels\n', labels)
    print('filenames\n', filenames)
    print('categorynames\n', categorynames)
    print('number_of_predictions', len(predictions))
    print('number_of_labels', len(labels))
    print('number_of_filenames', len(filenames))
    print('number_of_categorynames', len(categorynames))


if __name__ == '__main__':
    main()
