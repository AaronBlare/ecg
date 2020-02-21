import os
import math
import pandas as pd
from path import get_path
from scipy.stats import kruskal
from plot import boxplot

path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ecg_table_pa = ecg_table[pd.notnull(ecg_table['phenotypic_age'])]
ages = list(ecg_table['age'])
sex = list(ecg_table['sex'])
ages_pa = list(ecg_table_pa['age'])
delta_ages = list(ecg_table_pa['delta_age'])
code_blood_table = list(ecg_table['code_blood_table'])
parameters_names = list(ecg_table_pa.columns)[11:]

result_table_path = path + '/kruskal/table/'
if not os.path.exists(result_table_path):
    os.makedirs(result_table_path)

result_plot_path = path + '/kruskal/plot/'
if not os.path.exists(result_plot_path):
    os.makedirs(result_plot_path)

# Down subjects vs old subjects
down_subjects_ids = []
old_subjects_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('L'):
        old_subjects_ids.append(i)
    elif str(code).startswith('Q'):
        down_subjects_ids.append(i)
    else:
        continue

metrics_dict_down_old = {'param': [], 'kruskal_h': [], 'kruskal_pval': []}

for param_id in range(0, len(parameters_names)):

    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])

    curr_param = {'down': [], 'old': []}
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            if i in down_subjects_ids:
                curr_param['down'].append(param_values[i])
            elif i in old_subjects_ids:
                curr_param['old'].append(param_values[i])
            else:
                continue

    if len(set(curr_param['old'])) == 1 or len(set(curr_param['down'])) == 1:
        metrics_dict_down_old['param'].append(param_name)
        metrics_dict_down_old['kruskal_h'].append('nan')
        metrics_dict_down_old['kruskal_pval'].append('nan')
        continue

    results_down_old = kruskal(curr_param['down'], curr_param['old'])
    metrics_dict_down_old['param'].append(param_name)
    metrics_dict_down_old['kruskal_h'].append(results_down_old[0])
    metrics_dict_down_old['kruskal_pval'].append(results_down_old[1])

    if 0 < results_down_old[1] < 0.05:
        boxplot(curr_param, ['Down Syndrome subjects', 'Long-living subjects'], param_name,
                results_down_old[1], result_plot_path)

result_df_down_old = pd.DataFrame.from_dict(metrics_dict_down_old)
writer = pd.ExcelWriter(result_table_path + 'down_old.xlsx', engine='xlsxwriter')
result_df_down_old.to_excel(writer, index=False)
writer.save()

# Down subjects vs healthy siblings
down_subjects_ids = []
healthy_siblings_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('S') or str(code).startswith('B'):
        healthy_siblings_ids.append(i)
    elif str(code).startswith('Q'):
        down_subjects_ids.append(i)
    else:
        continue

metrics_dict_down_sibling = {'param': [], 'kruskal_h': [], 'kruskal_pval': []}

for param_id in range(0, len(parameters_names)):

    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])

    curr_param = {'down': [], 'sibling': []}
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            if i in down_subjects_ids:
                curr_param['down'].append(param_values[i])
            elif i in healthy_siblings_ids:
                curr_param['sibling'].append(param_values[i])
            else:
                continue

    if len(set(curr_param['sibling'])) == 1 or len(set(curr_param['down'])) == 1:
        metrics_dict_down_sibling['param'].append(param_name)
        metrics_dict_down_sibling['kruskal_h'].append('nan')
        metrics_dict_down_sibling['kruskal_pval'].append('nan')
        continue

    results_down_sibling = kruskal(curr_param['down'], curr_param['sibling'])
    metrics_dict_down_sibling['param'].append(param_name)
    metrics_dict_down_sibling['kruskal_h'].append(results_down_sibling[0])
    metrics_dict_down_sibling['kruskal_pval'].append(results_down_sibling[1])

    if 0 < results_down_sibling[1] < 0.05:
        boxplot(curr_param, ['Down Syndrome subjects', 'Healthy Siblings'], param_name,
                results_down_sibling[1], result_plot_path)

result_df_down_sibling = pd.DataFrame.from_dict(metrics_dict_down_sibling)
writer = pd.ExcelWriter(result_table_path + 'down_sibling.xlsx', engine='xlsxwriter')
result_df_down_sibling.to_excel(writer, index=False)
writer.save()

# Young subjects vs middle-age subjects vs old subjects (all healthy)
healthy_subjects = {'age': [], 'id': []}
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        continue
    else:
        healthy_subjects['age'].append(ages[i])
        healthy_subjects['id'].append(i)

young_subjects_ids = []
middle_subjects_ids = []
old_subjects_ids = []
for i in range(0, len(healthy_subjects['age'])):
    if healthy_subjects['age'][i] < 20:
        young_subjects_ids.append(healthy_subjects['id'][i])
    elif healthy_subjects['age'][i] > 60:
        old_subjects_ids.append(healthy_subjects['id'][i])
    else:
        middle_subjects_ids.append(healthy_subjects['id'][i])

metrics_dict_young_middle_old = {'param': [], 'kruskal_h': [], 'kruskal_pval': []}

for param_id in range(0, len(parameters_names)):

    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])

    curr_param = {'young': [], 'middle': [], 'old': []}
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            if i in young_subjects_ids:
                curr_param['young'].append(param_values[i])
            elif i in middle_subjects_ids:
                curr_param['middle'].append(param_values[i])
            elif i in old_subjects_ids:
                curr_param['old'].append(param_values[i])
            else:
                continue

    if len(set(curr_param['young'])) == 1 or len(set(curr_param['middle'])) == 1 or len(set(curr_param['old'])) == 1:
        metrics_dict_young_middle_old['param'].append(param_name)
        metrics_dict_young_middle_old['kruskal_h'].append('nan')
        metrics_dict_young_middle_old['kruskal_pval'].append('nan')
        continue

    results_young_middle_old = kruskal(curr_param['young'], curr_param['middle'], curr_param['old'])
    metrics_dict_young_middle_old['param'].append(param_name)
    metrics_dict_young_middle_old['kruskal_h'].append(results_young_middle_old[0])
    metrics_dict_young_middle_old['kruskal_pval'].append(results_young_middle_old[1])

    if 0 < results_young_middle_old[1] < 0.05:
        boxplot(curr_param, ['0-20 years', '20-60 years', '60-100 years'], param_name,
                results_young_middle_old[1], result_plot_path)

result_df_young_middle_old = pd.DataFrame.from_dict(metrics_dict_young_middle_old)
writer = pd.ExcelWriter(result_table_path + 'young_middle_old.xlsx', engine='xlsxwriter')
result_df_young_middle_old.to_excel(writer, index=False)
writer.save()

# Subjects with small delta age vs Subjects with big delta age
small_delta_ids = []
big_delta_ids = []
for i in range(0, len(delta_ages)):
    delta_age = delta_ages[i]
    if delta_age < 6.0:
        small_delta_ids.append(i)
    else:
        big_delta_ids.append(i)

metrics_dict_small_big_delta = {'param': [], 'kruskal_h': [], 'kruskal_pval': []}

for param_id in range(0, len(parameters_names)):

    param_name = parameters_names[param_id]
    param_values = list(ecg_table_pa[parameters_names[param_id]])

    curr_param = {'small_delta': [], 'big_delta': []}
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            if i in small_delta_ids:
                curr_param['small_delta'].append(param_values[i])
            elif i in big_delta_ids:
                curr_param['big_delta'].append(param_values[i])
            else:
                continue

    if len(set(curr_param['small_delta'])) == 1 or len(set(curr_param['big_delta'])) == 1:
        metrics_dict_small_big_delta['param'].append(param_name)
        metrics_dict_small_big_delta['kruskal_h'].append('nan')
        metrics_dict_small_big_delta['kruskal_pval'].append('nan')
        continue

    results_small_big_delta = kruskal(curr_param['small_delta'], curr_param['big_delta'])
    metrics_dict_small_big_delta['param'].append(param_name)
    metrics_dict_small_big_delta['kruskal_h'].append(results_small_big_delta[0])
    metrics_dict_small_big_delta['kruskal_pval'].append(results_small_big_delta[1])

    if 0 < results_small_big_delta[1] < 0.05:
        boxplot(curr_param, ['Subjects with small delta age', 'Subjects with big delta age'], param_name,
                results_small_big_delta[1], result_plot_path)

result_df_small_big_delta = pd.DataFrame.from_dict(metrics_dict_small_big_delta)
writer = pd.ExcelWriter(result_table_path + 'small_big_delta.xlsx', engine='xlsxwriter')
result_df_small_big_delta.to_excel(writer, index=False)
writer.save()

# Males vs Females
males_ids = []
females_ids = []
for i in range(0, len(sex)):
    if sex[i] == 'Male':
        males_ids.append(i)
    else:
        females_ids.append(i)

metrics_dict_male_female = {'param': [], 'kruskal_h': [], 'kruskal_pval': []}

for param_id in range(0, len(parameters_names)):

    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])

    curr_param = {'males': [], 'females': []}
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            if i in males_ids:
                curr_param['males'].append(param_values[i])
            elif i in females_ids:
                curr_param['females'].append(param_values[i])
            else:
                continue

    if len(set(curr_param['males'])) == 1 or len(set(curr_param['females'])) == 1:
        metrics_dict_male_female['param'].append(param_name)
        metrics_dict_male_female['kruskal_h'].append('nan')
        metrics_dict_male_female['kruskal_pval'].append('nan')
        continue

    results_male_female = kruskal(curr_param['males'], curr_param['females'])
    metrics_dict_male_female['param'].append(param_name)
    metrics_dict_male_female['kruskal_h'].append(results_male_female[0])
    metrics_dict_male_female['kruskal_pval'].append(results_male_female[1])

    if 0 < results_male_female[1] < 0.05:
        boxplot(curr_param, ['Males', 'Females'], param_name,
                results_male_female[1], result_plot_path)

result_df_male_female = pd.DataFrame.from_dict(metrics_dict_male_female)
writer = pd.ExcelWriter(result_table_path + 'males_females.xlsx', engine='xlsxwriter')
result_df_male_female.to_excel(writer, index=False)
writer.save()

# Down Males vs Down Females
down_males_ids = []
down_females_ids = []
for i in range(0, len(code_blood_table)):
    if str(code_blood_table[i]).startswith('Q'):
        if sex[i] == 'Male':
            down_males_ids.append(i)
        else:
            down_females_ids.append(i)
    else:
        continue

metrics_dict_down_male_female = {'param': [], 'kruskal_h': [], 'kruskal_pval': []}

for param_id in range(0, len(parameters_names)):

    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])

    curr_param = {'down_males': [], 'down_females': []}
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            if i in down_males_ids:
                curr_param['down_males'].append(param_values[i])
            elif i in down_females_ids:
                curr_param['down_females'].append(param_values[i])
            else:
                continue

    if len(set(curr_param['down_males'])) == 1 or len(set(curr_param['down_females'])) == 1:
        metrics_dict_down_male_female['param'].append(param_name)
        metrics_dict_down_male_female['kruskal_h'].append('nan')
        metrics_dict_down_male_female['kruskal_pval'].append('nan')
        continue

    results_down_male_female = kruskal(curr_param['down_males'], curr_param['down_females'])
    metrics_dict_down_male_female['param'].append(param_name)
    metrics_dict_down_male_female['kruskal_h'].append(results_down_male_female[0])
    metrics_dict_down_male_female['kruskal_pval'].append(results_down_male_female[1])

    if 0 < results_down_male_female[1] < 0.05:
        boxplot(curr_param, ['Down Syndrome Males', 'Down Syndrome Females'], param_name,
                results_down_male_female[1], result_plot_path)

result_df_down_male_female = pd.DataFrame.from_dict(metrics_dict_down_male_female)
writer = pd.ExcelWriter(result_table_path + 'down_males_females.xlsx', engine='xlsxwriter')
result_df_down_male_female.to_excel(writer, index=False)
writer.save()

# Males vs Females (all healthy)
healthy_subjects = {'sex': [], 'id': []}
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        continue
    else:
        healthy_subjects['sex'].append(sex[i])
        healthy_subjects['id'].append(i)

males_ids = []
females_ids = []
for i in range(0, len(healthy_subjects['sex'])):
    if healthy_subjects['sex'][i] == 'Male':
        males_ids.append(healthy_subjects['id'][i])
    else:
        females_ids.append(healthy_subjects['id'][i])

metrics_dict_male_female = {'param': [], 'kruskal_h': [], 'kruskal_pval': []}

for param_id in range(0, len(parameters_names)):

    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])

    curr_param = {'healthy_males': [], 'healthy_females': []}
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            if i in males_ids:
                curr_param['healthy_males'].append(param_values[i])
            elif i in females_ids:
                curr_param['healthy_females'].append(param_values[i])
            else:
                continue

    if len(set(curr_param['healthy_males'])) == 1 or len(set(curr_param['healthy_females'])) == 1:
        metrics_dict_male_female['param'].append(param_name)
        metrics_dict_male_female['kruskal_h'].append('nan')
        metrics_dict_male_female['kruskal_pval'].append('nan')
        continue

    results_healthy_male_female = kruskal(curr_param['healthy_males'], curr_param['healthy_females'])
    metrics_dict_male_female['param'].append(param_name)
    metrics_dict_male_female['kruskal_h'].append(results_healthy_male_female[0])
    metrics_dict_male_female['kruskal_pval'].append(results_healthy_male_female[1])

    if 0 < results_healthy_male_female[1] < 0.05:
        boxplot(curr_param, ['Healthy Males', 'Healthy Females'], param_name,
                results_healthy_male_female[1], result_plot_path)

result_df_healthy_male_female = pd.DataFrame.from_dict(metrics_dict_male_female)
writer = pd.ExcelWriter(result_table_path + 'healthy_males_females.xlsx', engine='xlsxwriter')
result_df_healthy_male_female.to_excel(writer, index=False)
writer.save()
