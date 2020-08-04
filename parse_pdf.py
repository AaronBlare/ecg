import os
import re
import pandas as pd
from path import get_path
from pdfminer.high_level import extract_text
from tabula import read_pdf

path = get_path() + '/data/pdf/'
data_dict = {'code': [], 'name': [], 'ecg_date': [], 'birth_date': [], 'age': [],
             'sex': [], 'height': [], 'weight': [], 'heart_rate': []}

for file in os.listdir(path):
    text = extract_text(path + file)
    text = re.sub(r'\n\s*\n', '\n', text)
    text_list = text.split('\n')

    name_list = re.findall(r"[\w']+", text_list[2].encode("latin-1").decode('cp1251'))
    if len(name_list) == 3:
        if len(name_list[1]) > len(name_list[-1]):
            name = name_list[0] + ' ' + name_list[-1] + ' ' + name_list[1]
        else:
            name = name_list[0] + ' ' + name_list[1] + ' ' + name_list[-1]
    elif len(name_list) == 2:
        name = name_list[0] + ' ' + name_list[1]
    else:
        name = name_list[0]
    data_dict['name'].append(name)

    code = text_list[3].encode("latin-1").decode('cp1251')
    data_dict['code'].append(code)

    if text_list[4] == 'Case No.:':

        ecg_date = text_list[5]
        data_dict['ecg_date'].append(ecg_date)

        birth_date = text_list[6]
        data_dict['birth_date'].append(birth_date)

        age = text_list[7].split(' ')[0]
        try:
            int(age)
            data_dict['age'].append(int(age))
        except ValueError:
            data_dict['age'].append('nan')

        sex = text_list[8]
        data_dict['sex'].append(sex)

        height = text_list[9].split(' ')[0]
        try:
            float(height)
            data_dict['height'].append(float(height))
        except ValueError:
            data_dict['height'].append('nan')

        weight = text_list[10].split(' ')[0]
        try:
            float(weight)
            data_dict['weight'].append(float(weight))
        except ValueError:
            data_dict['weight'].append('nan')

        heart_rate = text_list[21].split(' ')[0]
        try:
            int(heart_rate)
            data_dict['heart_rate'].append(int(heart_rate))
        except ValueError:
            data_dict['heart_rate'].append('nan')

        intervals_names = text_list[23:29]
        intervals = {key: '' for key in intervals_names}
        for i in range(29, 35):
            curr_interval_value = text_list[i]
            try:
                int(curr_interval_value.split(' ')[0])
                intervals[text_list[i - 6]] = int(curr_interval_value.split(' ')[0])
            except ValueError:
                intervals[text_list[i - 6]] = 'nan'

        intervals_names_full = []
        for i in range(0, len(intervals_names)):
            intervals_names_full.append('interval_' + intervals_names[i])
            if intervals_names_full[i] in data_dict:
                data_dict[intervals_names_full[i]].append(intervals[intervals_names[i]])
            else:
                data_dict[intervals_names_full[i]] = [intervals[intervals_names[i]]]

        axis_names = text_list[37:40]
        axis = {key: '' for key in axis_names}
        for i in range(40, 43):
            curr_axis_value = text_list[i]
            try:
                int(curr_axis_value.split(' ')[0])
                axis[text_list[i - 3]] = int(curr_axis_value.split(' ')[0])
            except ValueError:
                axis[text_list[i - 3]] = 'nan'

        axis_names_full = []
        for i in range(0, len(axis_names)):
            axis_names_full.append('axis_' + axis_names[i])
            if axis_names_full[i] in data_dict:
                data_dict[axis_names_full[i]].append(axis[axis_names[i]])
            else:
                data_dict[axis_names_full[i]] = [axis[axis_names[i]]]

    else:
        ecg_date = text_list[41]
        data_dict['ecg_date'].append(ecg_date)

        birth_date = text_list[4]
        data_dict['birth_date'].append(birth_date)

        age = text_list[5].split(' ')[0]
        try:
            int(age)
            data_dict['age'].append(int(age))
        except ValueError:
            data_dict['age'].append('nan')

        sex = text_list[6]
        data_dict['sex'].append(sex)

        height = text_list[7].split(' ')[0]
        try:
            float(height)
            data_dict['height'].append(float(height))
        except ValueError:
            data_dict['height'].append('nan')

        weight = text_list[8].split(' ')[0]
        try:
            float(weight)
            data_dict['weight'].append(float(weight))
        except ValueError:
            data_dict['weight'].append('nan')

        if text_list[19] == 'P':
            heart_rate = text_list[26].split(' ')[0]
            try:
                int(heart_rate)
                data_dict['heart_rate'].append(int(heart_rate))
            except ValueError:
                data_dict['heart_rate'].append('nan')

            intervals_names = text_list[28:34]
            intervals = {key: '' for key in intervals_names}
            for i in range(34, 40):
                curr_interval_value = text_list[i]
                try:
                    int(curr_interval_value.split(' ')[0])
                    intervals[text_list[i - 6]] = int(curr_interval_value.split(' ')[0])
                except ValueError:
                    intervals[text_list[i - 6]] = 'nan'

            intervals_names_full = []
            for i in range(0, len(intervals_names)):
                intervals_names_full.append('interval_' + intervals_names[i])
                if intervals_names_full[i] in data_dict:
                    data_dict[intervals_names_full[i]].append(intervals[intervals_names[i]])
                else:
                    data_dict[intervals_names_full[i]] = [intervals[intervals_names[i]]]

            axis_names = text_list[19:22]
            axis = {key: '' for key in axis_names}
            for i in range(22, 25):
                curr_axis_value = text_list[i]
                try:
                    int(curr_axis_value.split(' ')[0])
                    axis[text_list[i - 3]] = int(curr_axis_value.split(' ')[0])
                except ValueError:
                    axis[text_list[i - 3]] = 'nan'

            axis_names_full = []
            for i in range(0, len(axis_names)):
                axis_names_full.append('axis_' + axis_names[i])
                if axis_names_full[i] in data_dict:
                    data_dict[axis_names_full[i]].append(axis[axis_names[i]])
                else:
                    data_dict[axis_names_full[i]] = [axis[axis_names[i]]]

        else:
            heart_rate = text_list[19].split(' ')[0]
            try:
                int(heart_rate)
                data_dict['heart_rate'].append(int(heart_rate))
            except ValueError:
                data_dict['heart_rate'].append('nan')

            intervals_names = text_list[21:27]
            intervals = {key: '' for key in intervals_names}
            for i in range(27, 33):
                curr_interval_value = text_list[i]
                try:
                    int(curr_interval_value.split(' ')[0])
                    intervals[text_list[i - 6]] = int(curr_interval_value.split(' ')[0])
                except ValueError:
                    intervals[text_list[i - 6]] = 'nan'

            intervals_names_full = []
            for i in range(0, len(intervals_names)):
                intervals_names_full.append('interval_' + intervals_names[i])
                if intervals_names_full[i] in data_dict:
                    data_dict[intervals_names_full[i]].append(intervals[intervals_names[i]])
                else:
                    data_dict[intervals_names_full[i]] = [intervals[intervals_names[i]]]

            axis_names = text_list[35:38]
            axis = {key: '' for key in axis_names}
            for i in range(38, 41):
                curr_axis_value = text_list[i]
                try:
                    int(curr_axis_value.split(' ')[0])
                    axis[text_list[i - 3]] = int(curr_axis_value.split(' ')[0])
                except ValueError:
                    axis[text_list[i - 3]] = 'nan'

            axis_names_full = []
            for i in range(0, len(axis_names)):
                axis_names_full.append('axis_' + axis_names[i])
                if axis_names_full[i] in data_dict:
                    data_dict[axis_names_full[i]].append(axis[axis_names[i]])
                else:
                    data_dict[axis_names_full[i]] = [axis[axis_names[i]]]

    parameters_df = read_pdf(path + file, pages=2)
    parameters_names = list(parameters_df[0][list(parameters_df[0].columns)[0]])
    leads_names = list(parameters_df[0].columns)[1:]
    for lead in leads_names:
        for param in parameters_names:
            curr_key = param + '_lead_' + lead
            curr_index = parameters_names.index(param)
            curr_value = float(list(parameters_df[0][lead])[curr_index])
            if curr_key in data_dict:
                data_dict[curr_key].append(curr_value)
            else:
                data_dict[curr_key] = [curr_value]

    for i in range(1, len(list(data_dict.keys()))):
        if len(data_dict[list(data_dict.keys())[i]]) != len(data_dict[list(data_dict.keys())[i-1]]):
            print(file)

result_df = pd.DataFrame.from_dict(data_dict)
writer = pd.ExcelWriter(get_path() + '/ecg_data.xlsx', engine='xlsxwriter')
result_df.to_excel(writer, index=False)
writer.save()
