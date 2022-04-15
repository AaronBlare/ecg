import pandas as pd
from path import get_path
import xlsxwriter

path = get_path()

snp_file_name = 'L_Q_snp.xlsx'
ecg_file_name = 'ecg_data_info.xlsx'
epigen_file_name = 'pheno_xtd.xlsx'

snp_df = pd.read_excel(path + '/' + snp_file_name)
snp_subjects = set(snp_df['Code'])

ecg_df = pd.read_excel(path + '/' + ecg_file_name)
ecg_subjects = set(ecg_df['code_blood_table'])

epigen_df = pd.read_excel(path + '/' + epigen_file_name)
epigen_subjects = set(epigen_df['ID'])

intersection_dict = {'SNP_ECG_EPIGEN': [], 'SNP_ECG': [], 'SNP_EPIGEN': []}

snp_ecg_subjects = snp_subjects.intersection(ecg_subjects)
snp_epigen_subjects = snp_subjects.intersection(epigen_subjects)
snp_ecg_epigen_subjects = snp_ecg_subjects.intersection(epigen_subjects)

intersection_dict['SNP_ECG'] = list(snp_ecg_subjects)
intersection_dict['SNP_ECG'].sort()
intersection_dict['SNP_EPIGEN'] = list(snp_epigen_subjects)
intersection_dict['SNP_EPIGEN'].sort()
intersection_dict['SNP_ECG_EPIGEN'] = list(snp_ecg_epigen_subjects)
intersection_dict['SNP_ECG_EPIGEN'].sort()

with xlsxwriter.Workbook(path + '/intersect_subjects.xlsx') as workbook:
    worksheet = workbook.add_worksheet()
    for column_id in range(0, len(intersection_dict.keys())):
        curr_column = list(intersection_dict.keys())[column_id]
        worksheet.write(0, column_id, curr_column)

    for column_id in range(0, len(intersection_dict.keys())):
        curr_column = list(intersection_dict.keys())[column_id]
        for subject_id in range(0, len(intersection_dict[curr_column])):
            worksheet.write(subject_id + 1, column_id, intersection_dict[curr_column][subject_id])
