import numpy as np
import pandas as pd


df = pd.read_csv('20181015_logging_cooking_01.csv')
df.columns = ['frame', 'pred']

print(df['pred'])

print(np.array(df['pred']))

label_array = pd.Series(df['pred'])
print(label_array)
print(label_array[0:50])


record = []

start = 0
end = 50
df_record = pd.DataFrame({})
for i in range(int(len(label_array) / 50)):
    print(i)
    print(label_array[start:end])
    start += 50
    end += 50
    series = pd.Series(label_array[start:end])
    df_old = pd.concat(df_record, series)
    df_record = df_old

# for i in range(int(len(df) / 50)):
#     print(df[i*50:i*50+50])

# print('record')
# print(record)
# print(type(record))
# record = np.array(record)

# print(record.shape)

print(df_record)
