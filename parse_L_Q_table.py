import pandas as pd
from path import get_path
from datetime import datetime
import math

path = get_path()
L_Q_table_name = 'L_Q_2022.xlsx'
target_columns = {'Код': 'Code', 'Пол': 'Sex', 'Год рождения': 'Birth date', 'Дата забора': 'Test date',
                  'SNP9': 'SNP9', 'SNP12': 'SNP12', 'SNPCol': 'SNPCol', 'SNPMTHFR': 'SNPMTHFR', 'SNPApoB': 'SNPApoB'}
additional_columns = ['Age', 'Cardiorisk']

snps_columns = ['SNP9', 'SNP12', 'SNPCol', 'SNPMTHFR', 'SNPApoB']

final_columns = [target_columns[target_column] for target_column in target_columns.keys()]
final_columns.extend(additional_columns)
data_dict = {column_name: [] for column_name in final_columns}

L_Q_df = pd.read_excel(f"{path}/{L_Q_table_name}", sheet_name=None)
sheet_names = list(L_Q_df.keys())[1:]  # without first sheet "Инструкция"

for sheet_name in sheet_names:
    curr_sheet = L_Q_df[sheet_name]
    if set(target_columns.keys()).issubset(curr_sheet.columns):
        for target_column in target_columns.keys():
            target_column_eng = target_columns[target_column]
            curr_column = list(curr_sheet[target_column])
            if target_column_eng == 'Sex':
                for subject_id in range(0, len(curr_column)):
                    if curr_column[subject_id] == 'м':
                        curr_column[subject_id] = 'M'
                    elif curr_column[subject_id] == 'ж':
                        curr_column[subject_id] = 'F'
                    else:
                        curr_column[subject_id] = math.nan
            elif target_column_eng == 'Birth date' or target_column_eng == 'Test date':
                for subject_id in range(0, len(curr_column)):
                    if str(curr_column[subject_id]).split(' ')[0] in ['NaT', '-']:
                        curr_column[subject_id] = math.nan
                    elif len(str(curr_column[subject_id]).split(' ')) == 1:
                        curr_column[subject_id] = f"{str(curr_column[subject_id])}-01-01"
                    else:
                        curr_column[subject_id] = str(curr_column[subject_id]).split(' ')[0]
            data_dict[target_column_eng].extend(curr_column)

age = []
for subject_id in range(0, len(data_dict['Test date'])):
    if isinstance(data_dict['Test date'][subject_id], float):
        if math.isnan(data_dict['Test date'][subject_id]):
            curr_age = math.nan
    elif isinstance(data_dict['Birth date'][subject_id], float):
        if math.isnan(data_dict['Birth date'][subject_id]):
            curr_age = math.nan
    else:
        curr_test_date = datetime.strptime(data_dict['Test date'][subject_id], '%Y-%m-%d')
        curr_birth_date = datetime.strptime(data_dict['Birth date'][subject_id], '%Y-%m-%d')
        curr_age = (curr_test_date - curr_birth_date).days / 365.2425
    age.append(curr_age)
data_dict['Age'] = age

risk_score = []
for subject_id in range(0, len(data_dict['SNP9'])):
    curr_risk_score = 0
    for snp in snps_columns:
        if isinstance(data_dict[snp][subject_id], float):
            if math.isnan(data_dict[snp][subject_id]):
                curr_risk_score = math.nan
                break
        else:
            curr_risk_score += data_dict[snp][subject_id].count('G')
    risk_score.append(curr_risk_score)
data_dict['Cardiorisk'] = risk_score

result_df = pd.DataFrame.from_dict(data_dict)
result_df.to_excel(get_path() + '/parsed_L_Q.xlsx', index=False)
