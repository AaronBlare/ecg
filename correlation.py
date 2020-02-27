import os
import math
import pandas as pd
from path import get_path
from scipy.stats import spearmanr, pearsonr, pointbiserialr
from statsmodels.stats.multitest import multipletests

path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ecg_table_pa = ecg_table[pd.notnull(ecg_table['phenotypic_age'])]
ages = list(ecg_table['age'])
delta_ages = list(ecg_table_pa['delta_age'])
code_blood_table = list(ecg_table['code_blood_table'])
code_blood_table_pa = list(ecg_table_pa['code_blood_table'])
parameters_names = list(ecg_table_pa.columns)[11:]

result_path = path + '/correlation/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

metrics_dict_age = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': [],
                    'pointbiserial_coef': [], 'pointbiserial_pval': []}

metrics_dict_delta = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': [],
                      'pointbiserial_coef': [], 'pointbiserial_pval': []}
pvals_age = []
pvals_delta = []
for param_id in range(0, len(parameters_names)):
    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])
    param_values_pa = list(ecg_table_pa[parameters_names[param_id]])
    if len(set(param_values)) <= 1:
        metrics_dict_age['param'].append(param_name)
        metrics_dict_age['spearman_rho'].append('nan')
        metrics_dict_age['spearman_pval'].append('nan')
        metrics_dict_age['pearson_coef'].append('nan')
        metrics_dict_age['pearson_pval'].append('nan')
        metrics_dict_age['pointbiserial_coef'].append('nan')
        metrics_dict_age['pointbiserial_pval'].append('nan')

        if len(set(param_values_pa)) <= 1:

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['spearman_rho'].append('nan')
            metrics_dict_delta['spearman_pval'].append('nan')
            metrics_dict_delta['pearson_coef'].append('nan')
            metrics_dict_delta['pearson_pval'].append('nan')
            metrics_dict_delta['pointbiserial_coef'].append('nan')
            metrics_dict_delta['pointbiserial_pval'].append('nan')

        else:

            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(delta_ages[i])

            spearman_results_delta = spearmanr(curr_delta, curr_param_pa)
            pearson_results_delta = pearsonr(curr_delta, curr_param_pa)
            pointbiserial_results_delta = pointbiserialr(curr_delta, curr_param_pa)

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta['pearson_pval'].append(pearson_results_delta[1])
            metrics_dict_delta['pointbiserial_coef'].append(pointbiserial_results_delta[0])
            metrics_dict_delta['pointbiserial_pval'].append(pointbiserial_results_delta[1])
            pvals_delta.append(spearman_results_delta[1])

    else:

        curr_param = []
        curr_age = []
        for i in range(0, len(param_values)):
            if not math.isnan(param_values[i]):
                curr_param.append(param_values[i])
                curr_age.append(ages[i])

        spearman_results_age = spearmanr(curr_age, curr_param)
        pearson_results_age = pearsonr(curr_age, curr_param)
        pointbiserial_results_age = pointbiserialr(curr_age, curr_param)

        metrics_dict_age['param'].append(param_name)
        metrics_dict_age['spearman_rho'].append(spearman_results_age[0])
        metrics_dict_age['spearman_pval'].append(spearman_results_age[1])
        metrics_dict_age['pearson_coef'].append(pearson_results_age[0])
        metrics_dict_age['pearson_pval'].append(pearson_results_age[1])
        metrics_dict_age['pointbiserial_coef'].append(pointbiserial_results_age[0])
        metrics_dict_age['pointbiserial_pval'].append(pointbiserial_results_age[1])
        pvals_age.append(spearman_results_age[1])

        if len(set(param_values_pa)) <= 1:

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['spearman_rho'].append('nan')
            metrics_dict_delta['spearman_pval'].append('nan')
            metrics_dict_delta['pearson_coef'].append('nan')
            metrics_dict_delta['pearson_pval'].append('nan')
            metrics_dict_delta['pointbiserial_coef'].append('nan')
            metrics_dict_delta['pointbiserial_pval'].append('nan')

        else:

            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(delta_ages[i])

            spearman_results_delta = spearmanr(curr_delta, curr_param_pa)
            pearson_results_delta = pearsonr(curr_delta, curr_param_pa)
            pointbiserial_results_delta = pointbiserialr(curr_delta, curr_param_pa)

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta['pearson_pval'].append(pearson_results_delta[1])
            metrics_dict_delta['pointbiserial_coef'].append(pointbiserial_results_delta[0])
            metrics_dict_delta['pointbiserial_pval'].append(pointbiserial_results_delta[1])
            pvals_delta.append(spearman_results_delta[1])

reject, pvals_corr, alphacSidak, alphacBonf = multipletests(pvals_age, 0.05, method='fdr_bh')
pval_age_corrected = []
original_index_age = 0
for i in range(0, len(metrics_dict_age['param'])):
    if metrics_dict_age['spearman_pval'][i] == 'nan':
        pval_age_corrected.append('nan')
    else:
        pval_age_corrected.append(pvals_corr[original_index_age])
        original_index_age += 1
metrics_dict_age['spearman_pval_corr'] = pval_age_corrected

reject, pvals_corr, alphacSidak, alphacBonf = multipletests(pvals_delta, 0.05, method='fdr_bh')
pval_delta_corrected = []
original_index_delta = 0
for i in range(0, len(metrics_dict_delta['param'])):
    if metrics_dict_delta['spearman_pval'][i] == 'nan':
        pval_delta_corrected.append('nan')
    else:
        pval_delta_corrected.append(pvals_corr[original_index_delta])
        original_index_delta += 1
metrics_dict_delta['spearman_pval_corr'] = pval_delta_corrected

result_df_age = pd.DataFrame.from_dict(metrics_dict_age)
writer = pd.ExcelWriter(result_path + 'correlation_age.xlsx', engine='xlsxwriter')
result_df_age.to_excel(writer, index=False)
writer.save()

result_df_delta = pd.DataFrame.from_dict(metrics_dict_delta)
writer = pd.ExcelWriter(result_path + 'correlation_delta.xlsx', engine='xlsxwriter')
result_df_delta.to_excel(writer, index=False)
writer.save()

metrics_dict_age_healthy = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [],
                            'pearson_pval': [], 'pointbiserial_coef': [], 'pointbiserial_pval': []}

metrics_dict_delta_healthy = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [],
                              'pearson_pval': [], 'pointbiserial_coef': [], 'pointbiserial_pval': []}

pvals_age = []
pvals_delta = []
# Spearman for healthy subjects

healthy_ids = {'age': [], 'delta': []}
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        continue
    else:
        healthy_ids['age'].append(i)
for i in range(0, len(code_blood_table_pa)):
    code = code_blood_table_pa[i]
    if str(code).startswith('Q'):
        continue
    else:
        healthy_ids['delta'].append(i)

for param_id in range(0, len(parameters_names)):
    param_name = parameters_names[param_id]
    param_values = []
    healthy_ages = []
    for i in range(0, len(list(ecg_table[parameters_names[param_id]]))):
        curr_param_value = list(ecg_table[parameters_names[param_id]])[i]
        if not math.isnan(curr_param_value):
            if i in healthy_ids['age']:
                param_values.append(curr_param_value)
                healthy_ages.append(ages[i])

    param_values_pa = []
    healthy_delta_ages = []
    for i in range(0, len(list(ecg_table_pa[parameters_names[param_id]]))):
        curr_param_value = list(ecg_table_pa[parameters_names[param_id]])[i]
        if not math.isnan(curr_param_value):
            if i in healthy_ids['delta']:
                param_values_pa.append(curr_param_value)
                healthy_delta_ages.append(delta_ages[i])

    if len(set(param_values)) <= 1:
        metrics_dict_age_healthy['param'].append(param_name)
        metrics_dict_age_healthy['spearman_rho'].append('nan')
        metrics_dict_age_healthy['spearman_pval'].append('nan')
        metrics_dict_age_healthy['pearson_coef'].append('nan')
        metrics_dict_age_healthy['pearson_pval'].append('nan')
        metrics_dict_age_healthy['pointbiserial_coef'].append('nan')
        metrics_dict_age_healthy['pointbiserial_pval'].append('nan')

        if len(set(param_values_pa)) <= 1:

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['spearman_rho'].append('nan')
            metrics_dict_delta_healthy['spearman_pval'].append('nan')
            metrics_dict_delta_healthy['pearson_coef'].append('nan')
            metrics_dict_delta_healthy['pearson_pval'].append('nan')
            metrics_dict_delta_healthy['pointbiserial_coef'].append('nan')
            metrics_dict_delta_healthy['pointbiserial_pval'].append('nan')

        else:

            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(healthy_delta_ages[i])

            spearman_results_delta = spearmanr(curr_delta, curr_param_pa)
            pearson_results_delta = pearsonr(curr_delta, curr_param_pa)
            pointbiserial_results_delta = pointbiserialr(curr_delta, curr_param_pa)

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta_healthy['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta_healthy['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta_healthy['pearson_pval'].append(pearson_results_delta[1])
            metrics_dict_delta_healthy['pointbiserial_coef'].append(pointbiserial_results_delta[0])
            metrics_dict_delta_healthy['pointbiserial_pval'].append(pointbiserial_results_delta[1])
            pvals_delta.append(spearman_results_delta[1])

    else:

        curr_param = []
        curr_age = []
        for i in range(0, len(param_values)):
            if not math.isnan(param_values[i]):
                curr_param.append(param_values[i])
                curr_age.append(healthy_ages[i])

        spearman_results_age = spearmanr(curr_age, curr_param)
        pearson_results_age = pearsonr(curr_age, curr_param)
        pointbiserial_results_age = pointbiserialr(curr_age, curr_param)

        metrics_dict_age_healthy['param'].append(param_name)
        metrics_dict_age_healthy['spearman_rho'].append(spearman_results_age[0])
        metrics_dict_age_healthy['spearman_pval'].append(spearman_results_age[1])
        metrics_dict_age_healthy['pearson_coef'].append(pearson_results_age[0])
        metrics_dict_age_healthy['pearson_pval'].append(pearson_results_age[1])
        metrics_dict_age_healthy['pointbiserial_coef'].append(pointbiserial_results_age[0])
        metrics_dict_age_healthy['pointbiserial_pval'].append(pointbiserial_results_age[1])
        pvals_age.append(spearman_results_age[1])

        if len(set(param_values_pa)) <= 1:

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['spearman_rho'].append('nan')
            metrics_dict_delta_healthy['spearman_pval'].append('nan')
            metrics_dict_delta_healthy['pearson_coef'].append('nan')
            metrics_dict_delta_healthy['pearson_pval'].append('nan')
            metrics_dict_delta_healthy['pointbiserial_coef'].append('nan')
            metrics_dict_delta_healthy['pointbiserial_pval'].append('nan')

        else:

            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(healthy_delta_ages[i])

            spearman_results_delta = spearmanr(curr_delta, curr_param_pa)
            pearson_results_delta = pearsonr(curr_delta, curr_param_pa)
            pointbiserial_results_delta = pointbiserialr(curr_delta, curr_param_pa)

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta_healthy['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta_healthy['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta_healthy['pearson_pval'].append(pearson_results_delta[1])
            metrics_dict_delta_healthy['pointbiserial_coef'].append(pointbiserial_results_delta[0])
            metrics_dict_delta_healthy['pointbiserial_pval'].append(pointbiserial_results_delta[1])
            pvals_delta.append(spearman_results_delta[1])

reject, pvals_corr, alphacSidak, alphacBonf = multipletests(pvals_age, 0.05, method='fdr_bh')
pval_age_corrected = []
original_index_age = 0
for i in range(0, len(metrics_dict_age_healthy['param'])):
    if metrics_dict_age_healthy['spearman_pval'][i] == 'nan':
        pval_age_corrected.append('nan')
    else:
        pval_age_corrected.append(pvals_corr[original_index_age])
        original_index_age += 1
metrics_dict_age_healthy['spearman_pval_corr'] = pval_age_corrected

reject, pvals_corr, alphacSidak, alphacBonf = multipletests(pvals_delta, 0.05, method='fdr_bh')
pval_delta_corrected = []
original_index_delta = 0
for i in range(0, len(metrics_dict_delta_healthy['param'])):
    if metrics_dict_delta_healthy['spearman_pval'][i] == 'nan':
        pval_delta_corrected.append('nan')
    else:
        pval_delta_corrected.append(pvals_corr[original_index_delta])
        original_index_delta += 1
metrics_dict_delta_healthy['spearman_pval_corr'] = pval_delta_corrected

result_df_age = pd.DataFrame.from_dict(metrics_dict_age_healthy)
writer = pd.ExcelWriter(result_path + 'healthy_correlation_age.xlsx', engine='xlsxwriter')
result_df_age.to_excel(writer, index=False)
writer.save()

result_df_delta = pd.DataFrame.from_dict(metrics_dict_delta_healthy)
writer = pd.ExcelWriter(result_path + 'healthy_correlation_delta.xlsx', engine='xlsxwriter')
result_df_delta.to_excel(writer, index=False)
writer.save()

metrics_dict_age_down = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [],
                         'pearson_pval': [], 'pointbiserial_coef': [], 'pointbiserial_pval': []}

metrics_dict_delta_down = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [],
                           'pearson_pval': [], 'pointbiserial_coef': [], 'pointbiserial_pval': []}

pvals_age = []
pvals_delta = []
# Spearman for subjects with Down Syndrome

down_syndrome_ids = {'age': [], 'delta': []}
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        down_syndrome_ids['age'].append(i)
    else:
        continue
for i in range(0, len(code_blood_table_pa)):
    code = code_blood_table_pa[i]
    if str(code).startswith('Q'):
        down_syndrome_ids['delta'].append(i)
    else:
        continue

for param_id in range(0, len(parameters_names)):
    param_name = parameters_names[param_id]
    param_values = []
    down_ages = []
    for i in range(0, len(list(ecg_table[parameters_names[param_id]]))):
        curr_param_value = list(ecg_table[parameters_names[param_id]])[i]
        if not math.isnan(curr_param_value):
            if i in down_syndrome_ids['age']:
                param_values.append(curr_param_value)
                down_ages.append(ages[i])

    param_values_pa = []
    down_delta_ages = []
    for i in range(0, len(list(ecg_table_pa[parameters_names[param_id]]))):
        curr_param_value = list(ecg_table_pa[parameters_names[param_id]])[i]
        if not math.isnan(curr_param_value):
            if i in down_syndrome_ids['delta']:
                param_values_pa.append(curr_param_value)
                down_delta_ages.append(delta_ages[i])

    if len(set(param_values)) <= 1:
        metrics_dict_age_down['param'].append(param_name)
        metrics_dict_age_down['spearman_rho'].append('nan')
        metrics_dict_age_down['spearman_pval'].append('nan')
        metrics_dict_age_down['pearson_coef'].append('nan')
        metrics_dict_age_down['pearson_pval'].append('nan')
        metrics_dict_age_down['pointbiserial_coef'].append('nan')
        metrics_dict_age_down['pointbiserial_pval'].append('nan')

        if len(set(param_values_pa)) <= 1:

            metrics_dict_delta_down['param'].append(param_name)
            metrics_dict_delta_down['spearman_rho'].append('nan')
            metrics_dict_delta_down['spearman_pval'].append('nan')
            metrics_dict_delta_down['pearson_coef'].append('nan')
            metrics_dict_delta_down['pearson_pval'].append('nan')
            metrics_dict_delta_down['pointbiserial_coef'].append('nan')
            metrics_dict_delta_down['pointbiserial_pval'].append('nan')

        else:

            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(down_delta_ages[i])

            spearman_results_delta = spearmanr(curr_delta, curr_param_pa)
            pearson_results_delta = pearsonr(curr_delta, curr_param_pa)
            pointbiserial_results_delta = pointbiserialr(curr_delta, curr_param_pa)

            metrics_dict_delta_down['param'].append(param_name)
            metrics_dict_delta_down['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta_down['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta_down['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta_down['pearson_pval'].append(pearson_results_delta[1])
            metrics_dict_delta_down['pointbiserial_coef'].append(pointbiserial_results_delta[0])
            metrics_dict_delta_down['pointbiserial_pval'].append(pointbiserial_results_delta[1])
            if not math.isnan(spearman_results_delta[1]):
                pvals_delta.append(spearman_results_delta[1])

    else:

        curr_param = []
        curr_age = []
        for i in range(0, len(param_values)):
            if not math.isnan(param_values[i]):
                curr_param.append(param_values[i])
                curr_age.append(down_ages[i])

        spearman_results_age = spearmanr(curr_age, curr_param)
        pearson_results_age = pearsonr(curr_age, curr_param)
        pointbiserial_results_age = pointbiserialr(curr_age, curr_param)

        metrics_dict_age_down['param'].append(param_name)
        metrics_dict_age_down['spearman_rho'].append(spearman_results_age[0])
        metrics_dict_age_down['spearman_pval'].append(spearman_results_age[1])
        metrics_dict_age_down['pearson_coef'].append(pearson_results_age[0])
        metrics_dict_age_down['pearson_pval'].append(pearson_results_age[1])
        metrics_dict_age_down['pointbiserial_coef'].append(pointbiserial_results_age[0])
        metrics_dict_age_down['pointbiserial_pval'].append(pointbiserial_results_age[1])
        if not math.isnan(spearman_results_age[1]):
            pvals_age.append(spearman_results_age[1])

        if len(set(param_values_pa)) <= 1:

            metrics_dict_delta_down['param'].append(param_name)
            metrics_dict_delta_down['spearman_rho'].append('nan')
            metrics_dict_delta_down['spearman_pval'].append('nan')
            metrics_dict_delta_down['pearson_coef'].append('nan')
            metrics_dict_delta_down['pearson_pval'].append('nan')
            metrics_dict_delta_down['pointbiserial_coef'].append('nan')
            metrics_dict_delta_down['pointbiserial_pval'].append('nan')

        else:

            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(down_delta_ages[i])

            spearman_results_delta = spearmanr(curr_delta, curr_param_pa)
            pearson_results_delta = pearsonr(curr_delta, curr_param_pa)
            pointbiserial_results_delta = pointbiserialr(curr_delta, curr_param_pa)

            metrics_dict_delta_down['param'].append(param_name)
            metrics_dict_delta_down['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta_down['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta_down['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta_down['pearson_pval'].append(pearson_results_delta[1])
            metrics_dict_delta_down['pointbiserial_coef'].append(pointbiserial_results_delta[0])
            metrics_dict_delta_down['pointbiserial_pval'].append(pointbiserial_results_delta[1])
            if not math.isnan(spearman_results_delta[1]):
                pvals_delta.append(spearman_results_delta[1])

reject, pvals_corr, alphacSidak, alphacBonf = multipletests(pvals_age, 0.05, method='fdr_bh')
pval_age_corrected = []
original_index_age = 0
for i in range(0, len(metrics_dict_age_down['param'])):
    if metrics_dict_age_down['spearman_pval'][i] == 'nan' or math.isnan(metrics_dict_age_down['spearman_pval'][i]):
        pval_age_corrected.append('nan')
    else:
        pval_age_corrected.append(pvals_corr[original_index_age])
        original_index_age += 1
metrics_dict_age_down['spearman_pval_corr'] = pval_age_corrected

reject, pvals_corr, alphacSidak, alphacBonf = multipletests(pvals_delta, 0.05, method='fdr_bh')
pval_delta_corrected = []
original_index_delta = 0
for i in range(0, len(metrics_dict_delta_down['param'])):
    if metrics_dict_delta_down['spearman_pval'][i] == 'nan' or math.isnan(metrics_dict_delta_down['spearman_pval'][i]):
        pval_delta_corrected.append('nan')
    else:
        pval_delta_corrected.append(pvals_corr[original_index_delta])
        original_index_delta += 1
metrics_dict_delta_down['spearman_pval_corr'] = pval_delta_corrected

result_df_age = pd.DataFrame.from_dict(metrics_dict_age_down)
writer = pd.ExcelWriter(result_path + 'down_correlation_age.xlsx', engine='xlsxwriter')
result_df_age.to_excel(writer, index=False)
writer.save()

result_df_delta = pd.DataFrame.from_dict(metrics_dict_delta_down)
writer = pd.ExcelWriter(result_path + 'down_correlation_delta.xlsx', engine='xlsxwriter')
result_df_delta.to_excel(writer, index=False)
writer.save()
