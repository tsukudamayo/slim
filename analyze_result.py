import os
import glob

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


_DATA_DIR = '/media/panasonic/644E9C944E9C611A/tmp/data/tfrecord/food_256_dossari_20180807_3class_x10_constant'
_LABEL_FILE = 'labels.txt'


def convert_label_files_to_dict(data_dir, label_file):
    category_map = {}
    keys, values = [], []
    
    # read label file
    with open(os.path.join(data_dir, label_file)) as f:
        lines = f.readlines()
        f.close()

    # label file convert into python dictionary
    for line in lines:
        key_value = line.split(':')
        key = int(key_value[0])
        value = key_value[1].split()[0] # delete linefeed
        category_map[key] = value
    
    return category_map


def plot_confusion_matrix(true, pred):
    labels = sorted(list(set(true)))
    data_cmx = confusion_matrix(true, pred, labels=labels)
    df_cmx = pd.DataFrame(data_cmx, index=labels, columns=labels)

    # plot confusion matrix
    fig, ax = plt.subplots()
    ax.pcolor(df_cmx, cmap=cm.jet)
    data = df_cmx.values
    for x in range(data_cmx.shape[0]):
        for y in range(data_cmx.shape[1]):
            plt.text(x+0.5, y+0.5,
                     data[y, x],
                     horizontalalignment='center',
                     verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    fig.colorbar(ax.pcolor(df_cmx),ax=ax)
    plt.show()

    return


def plot_accuracy(df, category_map):
    for k, v in category_map.items():
        try:
            print('*'*10 + v + '*'*10)
            label_df = df[df['label'] == int(k)]
            preds = label_df['prediction']
            labels = label_df['label']
            acc = accuracy_score(preds, labels)
            print(v, acc)
            plt.bar(v, acc)
        except KeyError:
            pass
    
    plt.ylim(0.0, 1.1)
    plt.show()

    return


def main():
    # load category data
    category_map = convert_label_files_to_dict(_DATA_DIR, _LABEL_FILE)
    print('category map\n', category_map)

    # read file which written result that eval classifier
    read_file = sorted(glob.glob('./*result.csv'))
    print(read_file[-1])
    df = pd.read_csv(read_file[-1])
    preds = df['prediction']
    labels =  df['label']

    # analayze result
    print('accuracy_score\n', accuracy_score(preds, labels))
    plot_accuracy(df, category_map)
    print('classification_report\n', classification_report(preds, labels))
    print('confusion_matrix\n', confusion_matrix(preds, labels))
    plot_confusion_matrix(preds, labels)


if __name__ == '__main__':
    main()
