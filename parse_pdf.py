import os
import re
from path import get_path
from pdfminer.high_level import extract_text

path = get_path() + '/data/pdf/'
for file in os.listdir(path):
    text = extract_text(path + file)
    text = re.sub(r'\n\s*\n', '\n', text)
    text_list = text.split('\n')
    name_list = re.findall(r"[\w']+", text_list[2].encode("latin-1").decode('cp1251'))
    name = name_list[0] + ' ' + name_list[-1] + ' ' + name_list[1]
    code = text_list[3].encode("latin-1").decode('cp1251')
    ecg_date = text_list[5]
    birth_date = text_list[6]
    age = int(text_list[7].split(' ')[0])
    sex = text_list[8]
    height = float(text_list[9].split(' ')[0])
    weight = float(text_list[10].split(' ')[0])
    heart_rate = int(text_list[21].split(' ')[0])
    intervals = {key: '' for key in text_list[23:28]}
    for id in range(29, 35):
        intervals[text_list[id - 6]] = text_list[id]
    axis = {key: '' for key in text_list[37:39]}
    for id in range(40, 43):
        axis[text_list[id - 3]] = text_list[id]
    leads = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    parameters_names_indices = list(range(110, 118))
    parameters_names_indices.extend([316, 119, 120, 121, 326, 328, 329])
    parameters = {key: {lead: '' for lead in leads} for key in [text_list[i] for i in parameters_names_indices]}
