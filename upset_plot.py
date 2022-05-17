import pandas as pd
from upsetplot import UpSet, from_indicators, from_contents
import matplotlib.pyplot as plt

path = "E:/YandexDisk/pydnameth/datasets/GPL21145/GSEUNN/special/022_ml_data_cardio/"
path_save = "E:/YandexDisk/ECG/upset/"
data_types = ['ecg', 'sphy', 'snp']

data_indexes = {data_type: [] for data_type in data_types}
data_indexes['subjects'] = []
data_dict = {data_type: [] for data_type in data_types}
for data_type in data_types:
    curr_data = pd.read_excel(path + data_type + '/data.xlsx')
    curr_subjects = list(curr_data['index'])
    data_dict[data_type] = curr_subjects
    for subject in curr_subjects:
        if subject in data_indexes['subjects']:
            curr_index = data_indexes['subjects'].index(subject)
            data_indexes[data_type][curr_index] = True
        else:
            data_indexes['subjects'].append(subject)
            for dt in data_types:
                if dt == data_type:
                    data_indexes[dt].append(True)
                else:
                    data_indexes[dt].append(False)
"""
df = pd.DataFrame.from_dict(data_indexes)
fig = UpSet(from_indicators(data_types, data=df), show_counts=True, min_degree=1).plot()
plt.savefig(f"{path_save}upset.png", bbox_inches='tight')
plt.clf()
"""
df = from_contents(data_dict)
fig = UpSet(df, show_counts=True, min_degree=1).plot()
plt.savefig(f"{path_save}upset.png", bbox_inches='tight')
plt.clf()
