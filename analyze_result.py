import pandas as pd
import matplotlib.pyplot as plt
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix


df = pd.read_csv('20180731_result.csv')
preds = df['prediction']
labels =  df['label']

# print('accuracy_score\n', accuracy_score(preds, labels))
# print('classification_report\n', classification_report(preds, labels))
# print('confusion_matrix\n', confusion_matrix(preds, labels))
def calcurate_acc(preds, labels):
    count = 0
    for pred, label in zip(preds, labels):
        if pred == label:
            count += 1
        else:
            pass

    print('the number of data\n', len(df))
    print('the number of correct prediction', count)
    print('accuracy :', (count / len(preds)))
    
    return (count / len(preds))

calcurate_acc(preds, labels)

labels_map = {
  'broccoli'    : '0',
  'cucumber'    : '1',
  'eggplant'    : '2',
  'greenpepper' : '3',
  'lettuce'     : '4',
  'tomato'      : '5',
}

print(labels_map)

columns_list = df.columns
for k, v in labels_map.items():
    try:
        print('*'*10 + k + '*'*10)
        label_df = df[df['label'] == int(v)]
        preds = label_df['prediction']
        labels = label_df['label']
        acc = calcurate_acc(preds, labels)
        plt.bar(k, acc)
    except KeyError:
        pass

plt.ylim(0.0, 1.1)
plt.show()

