import os
import re
import pandas as pd
from path import get_path
from pdfminer.high_level import extract_text
from tabula import read_pdf

path = get_path() + '/data/pdf_2021/'
data_dict = {'code': [], 'name': [], 'ecg_date': [], 'ecg_time': [], 'birth_date': [], 'age': [],
             'sex': [], 'height': [], 'weight': [], 'heart_rate': []}

for file in os.listdir(path):
    print(file)
    text = extract_text(path + file)
    text = re.sub(r'\n\s*\n', '\n', text)
    text_list = text.split('\n')

    try:
        name_list = re.findall(r"[\w']+", text_list[2].encode("latin-1").decode('cp1251'))
    except UnicodeEncodeError:
        name_list = text_list[2].split(' ')
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

    try:
        code = text_list[3].encode("latin-1").decode('cp1251')
    except UnicodeEncodeError:
        code = text_list[3]
    data_dict['code'].append(code)

    if text_list[4] in ['Case No.:', '№ ист.бол.:']:

        ecg_date = text_list[5].split(' ')
        data_dict['ecg_date'].append(ecg_date[0])
        data_dict['ecg_time'].append(ecg_date[2])

        birth_date = text_list[12]
        data_dict['birth_date'].append(birth_date)

        age = text_list[13].split(' ')[0]
        try:
            int(age)
            data_dict['age'].append(int(age))
        except ValueError:
            data_dict['age'].append('nan')

        sex = text_list[14]
        if sex == 'Ж':
            sex = 'F'
        elif sex == 'М':
            sex = 'M'
        data_dict['sex'].append(sex)

        height = text_list[15].split(' ')[0]
        if ',' in height:
            height = height.replace(',', '.')
        try:
            float(height)
            data_dict['height'].append(float(height))
        except ValueError:
            data_dict['height'].append('nan')

        weight = text_list[16].split(' ')[0]
        if ',' in weight:
            weight = weight.replace(',', '.')
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

    elif text_list[3] in ['Case No.:', '№ ист.бол.:']:

        name = ''
        data_dict['name'][-1] = name
        code = text_list[2]
        data_dict['code'][-1] = code

        ecg_date = text_list[4].split(' ')
        data_dict['ecg_date'].append(ecg_date[0])
        data_dict['ecg_time'].append(ecg_date[2])

        birth_date = text_list[5]
        data_dict['birth_date'].append(birth_date)

        age = text_list[6].split(' ')[0]
        try:
            int(age)
            data_dict['age'].append(int(age))
        except ValueError:
            data_dict['age'].append('nan')

        sex = text_list[7]
        if sex == 'Ж':
            sex = 'F'
        elif sex == 'М':
            sex = 'M'
        data_dict['sex'].append(sex)

        height = text_list[8].split(' ')[0]
        if ',' in height:
            height = height.replace(',', '.')
        try:
            float(height)
            data_dict['height'].append(float(height))
        except ValueError:
            data_dict['height'].append('nan')

        weight = text_list[9].split(' ')[0]
        if ',' in weight:
            weight = weight.replace(',', '.')
        try:
            float(weight)
            data_dict['weight'].append(float(weight))
        except ValueError:
            data_dict['weight'].append('nan')

        heart_rate = text_list[20].split(' ')[0]
        try:
            int(heart_rate)
            data_dict['heart_rate'].append(int(heart_rate))
        except ValueError:
            data_dict['heart_rate'].append('nan')

        intervals_names = text_list[22:28]
        intervals = {key: '' for key in intervals_names}
        for i in range(28, 34):
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

        axis_names = text_list[36:39]
        axis = {key: '' for key in axis_names}
        for i in range(39, 42):
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

    elif text_list[0] not in ['Pat-Name:', 'Пациент:']:

        try:
            name_list = re.findall(r"[\w']+", text_list[0].encode("latin-1").decode('cp1251'))
        except UnicodeEncodeError:
            name_list = text_list[0].split(' ')
        if len(name_list) == 3:
            if len(name_list[1]) > len(name_list[-1]):
                name = name_list[0] + ' ' + name_list[-1] + ' ' + name_list[1]
            else:
                name = name_list[0] + ' ' + name_list[1] + ' ' + name_list[-1]
        elif len(name_list) == 2:
            name = name_list[0] + ' ' + name_list[1]
        else:
            name = name_list[0]
        data_dict['name'][-1] = name
        try:
            code = text_list[1].encode("latin-1").decode('cp1251')
        except UnicodeEncodeError:
            code = text_list[1]
        data_dict['code'][-1] = code

        ecg_date = text_list[41].split(' ')
        data_dict['ecg_date'].append(ecg_date[0])
        data_dict['ecg_time'].append(ecg_date[2])

        birth_date = text_list[2]
        data_dict['birth_date'].append(birth_date)

        age = text_list[3].split(' ')[0]
        try:
            int(age)
            data_dict['age'].append(int(age))
        except ValueError:
            data_dict['age'].append('nan')

        sex = text_list[4]
        if sex == 'Ж':
            sex = 'F'
        elif sex == 'М':
            sex = 'M'
        data_dict['sex'].append(sex)

        height = text_list[5].split(' ')[0]
        if ',' in height:
            height = height.replace(',', '.')
        try:
            float(height)
            data_dict['height'].append(float(height))
        except ValueError:
            data_dict['height'].append('nan')

        weight = text_list[6].split(' ')[0]
        if ',' in weight:
            weight = weight.replace(',', '.')
        try:
            float(weight)
            data_dict['weight'].append(float(weight))
        except ValueError:
            data_dict['weight'].append('nan')

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

    else:
        ecg_date = text_list[41].split(' ')
        data_dict['ecg_date'].append(ecg_date[0])
        data_dict['ecg_time'].append(ecg_date[2])

        birth_date = text_list[10]
        data_dict['birth_date'].append(birth_date)

        age = text_list[11].split(' ')[0]
        try:
            int(age)
            data_dict['age'].append(int(age))
        except ValueError:
            data_dict['age'].append('nan')

        sex = text_list[12]
        if sex == 'Ж':
            sex = 'F'
        elif sex == 'М':
            sex = 'M'
        data_dict['sex'].append(sex)

        height = text_list[13].split(' ')[0]
        if ',' in height:
            height = height.replace(',', '.')
        try:
            float(height)
            data_dict['height'].append(float(height))
        except ValueError:
            data_dict['height'].append('nan')

        weight = text_list[14].split(' ')[0]
        if ',' in weight:
            weight = weight.replace(',', '.')
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
            if param.endswith('.'):
                param_eng = param[:-1]
            else:
                param_eng = param
            if 'пол' in param:
                param_eng = param_eng.replace('пол', 'Pos')
            if 'ампл' in param:
                param_eng = param_eng.replace('ампл', 'Ampl')
            if 'отр' in param:
                param_eng = param_eng.replace('отр', 'Neg')
            if 'длит' in param:
                param_eng = param_eng.replace('длит', 'Dur')
            if 'интегр' in param:
                param_eng = param_eng.replace('интегр', 'Integ.')
            curr_key = param_eng + '_lead_' + lead
            curr_index = parameters_names.index(param)
            curr_value = list(parameters_df[0][lead])[curr_index]
            if ',' in curr_value:
                curr_value = float(curr_value.replace(',', '.'))
            else:
                curr_value = float(curr_value)
            if curr_key in data_dict:
                data_dict[curr_key].append(curr_value)
            else:
                data_dict[curr_key] = [curr_value]

    for i in range(1, len(list(data_dict.keys()))):
        if len(data_dict[list(data_dict.keys())[i]]) != len(data_dict[list(data_dict.keys())[i-1]]):
            print(file)

result_df = pd.DataFrame.from_dict(data_dict)
writer = pd.ExcelWriter(get_path() + '/ecg_data_2021.xlsx', engine='xlsxwriter')
result_df.to_excel(writer, index=False)
writer.save()
