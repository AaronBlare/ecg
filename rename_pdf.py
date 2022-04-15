import os
import re
import pandas as pd
from path import get_path
from pathlib import Path
from pdfminer.high_level import extract_text
import shutil

path = get_path() + '/data/pdf/'
ecg_table = pd.read_excel(get_path() + '/ecg_data_info.xlsx')
ecg_ru_codes = list(ecg_table['code'])
ecg_codes = list(ecg_table['code_blood_table'])

new_path = path + 'renamed/'
Path(new_path).mkdir(parents=True, exist_ok=True)

for file in os.listdir(path):
    if not os.path.isdir(path + file):
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

        code = text_list[3].encode("latin-1").decode('cp1251')

        if text_list[4] == 'Case No.:':
            ecg_date_time = text_list[5].split(' ')
            ecg_date = ecg_date_time[0]
            ecg_time = ecg_date_time[2]

        elif text_list[3] == 'Case No.:':
            code = text_list[2]
            ecg_date_time = text_list[4].split(' ')
            ecg_date = ecg_date_time[0]
            ecg_time = ecg_date_time[2]

        elif text_list[1] == 'Case No.:':
            print(file)
            continue

        elif text_list[0] != 'Pat-Name:':
            name_list = re.findall(r"[\w']+", text_list[0].encode("latin-1").decode('cp1251'))
            if len(name_list) == 3:
                if len(name_list[1]) > len(name_list[-1]):
                    name = name_list[0] + ' ' + name_list[-1] + ' ' + name_list[1]
                else:
                    name = name_list[0] + ' ' + name_list[1] + ' ' + name_list[-1]
            elif len(name_list) == 2:
                name = name_list[0] + ' ' + name_list[1]
            else:
                name = name_list[0]

            code = text_list[1].encode("latin-1").decode('cp1251')
            ecg_date_time = text_list[41].split(' ')
            ecg_date = ecg_date_time[0]
            ecg_time = ecg_date_time[2]
        else:
            ecg_date_time = text_list[41].split(' ')
            ecg_date = ecg_date_time[0]
            ecg_time = ecg_date_time[2]

        if code in ecg_ru_codes:
            ru_code_index = ecg_ru_codes.index(code)
            blood_table_code = ecg_codes[ru_code_index]

            if len(blood_table_code.split('/')) > 1:
                blood_table_code = ''.join(blood_table_code.split('/'))

            src_file = path + file
            dst_file = f"{new_path}{blood_table_code}_{'-'.join(ecg_date.split('.'))}_{'-'.join(ecg_time.split(':'))}.pdf"
            if not os.path.isfile(dst_file):
                shutil.copy(src_file, dst_file)
        else:
            print(file)
