import pandas as pd
from path import get_path

path = get_path()

data_dict = pd.read_excel(f'{path}/L_and_Q.xlsx', sheet_name=None, engine='openpyxl')
sheets_names = list(data_dict.keys())

subjects_df = pd.read_excel(f'{path}/ecg_data_info.xlsx', engine='openpyxl')
subjects = list(subjects_df['code_blood_table'])

id_sheet_dict = {}
for sheet_name in sheets_names:
    curr_sheet = data_dict[sheet_name]
    curr_codes = list(curr_sheet['Код'])
    for code in curr_codes:
        id_sheet_dict[code] = sheet_name

snp_dict = {'ID': [], 'SNP9': [], 'SNP12': [], 'SNPCol': [], 'SNPMTHFR': [], 'SNPApoB': []}

for subject in subjects:

    snp_dict['ID'].append(subject)
    sheet_name = id_sheet_dict[subject]
    curr_sheet = data_dict[sheet_name]
    subject_id = list(curr_sheet['Код']).index(subject)

    if 'SNP9' in curr_sheet:
        curr_SNP9 = curr_sheet['SNP9'][subject_id]
        if curr_SNP9 == 'AA':
            snp_dict['SNP9'].append(0)
        elif curr_SNP9 == 'AG':
            snp_dict['SNP9'].append(1)
        elif curr_SNP9 == 'GA':
            snp_dict['SNP9'].append(2)
        elif curr_SNP9 == 'GG':
            snp_dict['SNP9'].append(3)
        else:
            snp_dict['SNP9'].append('')
    else:
        snp_dict['SNP9'].append('')

    if 'SNP12' in curr_sheet:
        SNP12 = curr_sheet['SNP12'][subject_id]
        if SNP12 == 'AA':
            snp_dict['SNP12'].append(0)
        elif SNP12 == 'AG':
            snp_dict['SNP12'].append(1)
        elif SNP12 == 'GA':
            snp_dict['SNP12'].append(2)
        elif SNP12 == 'GG':
            snp_dict['SNP12'].append(3)
        else:
            snp_dict['SNP12'].append('')
    else:
        snp_dict['SNP12'].append('')

    if 'SNPCol' in curr_sheet:
        SNPCol = curr_sheet['SNPCol'][subject_id]
        if SNPCol == 'AA':
            snp_dict['SNPCol'].append(0)
        elif SNPCol == 'AG':
            snp_dict['SNPCol'].append(1)
        elif SNPCol == 'GA':
            snp_dict['SNPCol'].append(2)
        elif SNPCol == 'GG':
            snp_dict['SNPCol'].append(3)
        else:
            snp_dict['SNPCol'].append('')
    else:
        snp_dict['SNPCol'].append('')

    if 'SNPMTHFR' in curr_sheet:
        SNPMTHFR = curr_sheet['SNPMTHFR'][subject_id]
        if SNPMTHFR == 'AA':
            snp_dict['SNPMTHFR'].append(0)
        elif SNPMTHFR == 'AG':
            snp_dict['SNPMTHFR'].append(1)
        elif SNPMTHFR == 'GA':
            snp_dict['SNPMTHFR'].append(2)
        elif SNPMTHFR == 'GG':
            snp_dict['SNPMTHFR'].append(3)
        else:
            snp_dict['SNPMTHFR'].append('')
    else:
        snp_dict['SNPMTHFR'].append('')

    if 'SNPApoB' in curr_sheet:
        SNPApoB = curr_sheet['SNPApoB'][subject_id]
        if SNPApoB == 'AA':
            snp_dict['SNPApoB'].append(0)
        elif SNPApoB == 'AG':
            snp_dict['SNPApoB'].append(1)
        elif SNPApoB == 'GA':
            snp_dict['SNPApoB'].append(2)
        elif SNPApoB == 'GG':
            snp_dict['SNPApoB'].append(3)
        else:
            snp_dict['SNPApoB'].append('')
    else:
        snp_dict['SNPApoB'].append('')

result_df = pd.DataFrame.from_dict(snp_dict)
writer = pd.ExcelWriter(get_path() + '/snp_ecg_data.xlsx', engine='xlsxwriter')
result_df.to_excel(writer, index=False)
writer.save()

subjects_df = subjects_df.assign(SNP9=pd.Series(snp_dict['SNP9']).values)
subjects_df = subjects_df.assign(SNP12=pd.Series(snp_dict['SNP12']).values)
subjects_df = subjects_df.assign(SNPCol=pd.Series(snp_dict['SNPCol']).values)
subjects_df = subjects_df.assign(SNPMTHFR=pd.Series(snp_dict['SNPMTHFR']).values)
subjects_df = subjects_df.assign(SNPApoB=pd.Series(snp_dict['SNPApoB']).values)

writer = pd.ExcelWriter(get_path() + '/ecg_snp_data_info.xlsx', engine='xlsxwriter')
subjects_df.to_excel(writer, index=False)
writer.save()
