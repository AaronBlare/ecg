import os
import math
import pandas as pd
from path import get_path
from scipy.stats import spearmanr, pearsonr, pointbiserialr

path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ecg_table_pa = ecg_table[pd.notnull(ecg_table['phenotypic_age'])]
ages = list(ecg_table_pa['age'])
delta_ages = list(ecg_table_pa['delta_age'])
parameters_names = list(ecg_table_pa.columns)[11:]

metrics_dict_age = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': [],
                    'pointbiserial_coef': [], 'pointbiserial_pval': []}

metrics_dict_delta = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': [],
                      'pointbiserial_coef': [], 'pointbiserial_pval': []}

for param_id in range(0, len(parameters_names)):
    param_name = parameters_names[param_id]
    param_values = list(ecg_table_pa[parameters_names[param_id]])
    if len(set(param_values)) == 1:
        metrics_dict_age['param'].append(param_name)
        metrics_dict_age['spearman_rho'].append(0)
        metrics_dict_age['spearman_pval'].append(0)
        metrics_dict_age['pearson_coef'].append(0)
        metrics_dict_age['pearson_pval'].append(0)
        metrics_dict_age['pointbiserial_coef'].append(0)
        metrics_dict_age['pointbiserial_pval'].append(0)

        metrics_dict_delta['param'].append(param_name)
        metrics_dict_delta['spearman_rho'].append(0)
        metrics_dict_delta['spearman_pval'].append(0)
        metrics_dict_delta['pearson_coef'].append(0)
        metrics_dict_delta['pearson_pval'].append(0)
        metrics_dict_delta['pointbiserial_coef'].append(0)
        metrics_dict_delta['pointbiserial_pval'].append(0)
        continue

    curr_param = []
    curr_age = []
    curr_delta = []
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            curr_param.append(param_values[i])
            curr_age.append(ages[i])
            curr_delta.append(delta_ages[i])

    spearman_results_age = spearmanr(curr_age, curr_param)
    spearman_results_delta = spearmanr(curr_delta, curr_param)

    pearson_results_age = pearsonr(curr_age, curr_param)
    pearson_results_delta = pearsonr(curr_age, curr_param)

    pointbiserial_results_age = pointbiserialr(curr_age, curr_param)
    pointbiserial_results_delta = pointbiserialr(curr_delta, curr_param)

    metrics_dict_age['param'].append(param_name)
    metrics_dict_age['spearman_rho'].append(spearman_results_age[0])
    metrics_dict_age['spearman_pval'].append(spearman_results_age[1])
    metrics_dict_age['pearson_coef'].append(pearson_results_age[0])
    metrics_dict_age['pearson_pval'].append(pearson_results_age[1])
    metrics_dict_age['pointbiserial_coef'].append(pointbiserial_results_age[0])
    metrics_dict_age['pointbiserial_pval'].append(pointbiserial_results_age[1])

    metrics_dict_delta['param'].append(param_name)
    metrics_dict_delta['spearman_rho'].append(spearman_results_delta[0])
    metrics_dict_delta['spearman_pval'].append(spearman_results_delta[1])
    metrics_dict_delta['pearson_coef'].append(pearson_results_delta[0])
    metrics_dict_delta['pearson_pval'].append(pearson_results_delta[1])
    metrics_dict_delta['pointbiserial_coef'].append(pointbiserial_results_delta[0])
    metrics_dict_delta['pointbiserial_pval'].append(pointbiserial_results_delta[1])

result_path = path + '/correlation/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

result_df_age = pd.DataFrame.from_dict(metrics_dict_age)
writer = pd.ExcelWriter(result_path + 'correlation_age.xlsx', engine='xlsxwriter')
result_df_age.to_excel(writer, index=False)
writer.save()

result_df_delta = pd.DataFrame.from_dict(metrics_dict_delta)
writer = pd.ExcelWriter(result_path + 'correlation_delta.xlsx', engine='xlsxwriter')
result_df_delta.to_excel(writer, index=False)
writer.save()
