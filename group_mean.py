import math
import pandas as pd
import numpy as np
from path import get_path
from scipy.stats import iqr

path = get_path()
data_file = path + '/ecg_data.xlsx'
df = pd.read_excel(data_file)
data_dict = df.to_dict('list')

subjects = {'Long-living subjects': [], 'Subjects with Down Syndrome': [],
            'Parents of Down Syndrome subjects': [], 'Siblings of Down Syndrome subjects': []}
for i in range(0, len(data_dict['age'])):
    curr_age = data_dict['age'][i]
    if curr_age > 80.0:
        subjects['Long-living subjects'].append(i)

for i in range(0, len(data_dict['code'])):
    curr_code = data_dict['code'][i]
    if curr_code.startswith('ку'):
        subjects['Subjects with Down Syndrome'].append(i)
    elif curr_code.startswith('мк') or curr_code.startswith('фк') or curr_code.startswith('Мк') or curr_code.startswith(
            'Фк') or curr_code.startswith('МК') or curr_code.startswith('ФК'):
        subjects['Parents of Down Syndrome subjects'].append(i)
    elif curr_code.startswith('ск') or curr_code.startswith('с1к') or curr_code.startswith(
            'с2к') or curr_code.startswith('бк') or curr_code.startswith('Ск') or curr_code.startswith('Бк'):
        subjects['Siblings of Down Syndrome subjects'].append(i)

mean_data = {'group': [], 'num_subjects': []}
keys_to_remove = ['code', 'name', 'ecg_date', 'birth_date', 'sex']
for key in data_dict:
    if key not in keys_to_remove:
        mean_data[key + ' mean'] = []
        mean_data[key + ' std'] = []
        mean_data[key + ' IQR'] = []

for group in subjects:
    indexes = subjects[group]
    mean_data['group'].append(group)
    mean_data['num_subjects'].append(len(indexes))
    for key in data_dict:
        if key + ' mean' in mean_data:
            curr_data = [data_dict[key][i] for i in indexes]
            curr_values = []
            for item in curr_data:
                if not math.isnan(item):
                    curr_values.append(float(item))
            curr_mean = np.mean(curr_values)
            curr_std = np.std(curr_values)
            curr_iqr = iqr(curr_values)
            mean_data[key + ' mean'].append(curr_mean)
            mean_data[key + ' std'].append(curr_std)
            mean_data[key + ' IQR'].append(curr_iqr)

result_df = pd.DataFrame.from_dict(mean_data)
writer = pd.ExcelWriter(get_path() + '/mean_characteristics.xlsx', engine='xlsxwriter')
result_df.to_excel(writer, index=False)
writer.save()
