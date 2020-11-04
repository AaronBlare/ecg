import os
import pandas as pd
from path import get_path
from functions import calculate_correlation_with_age, multiple_test_correction
from save import save_dict_to_xlsx


path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ages = list(ecg_table['age'])
delta_ages = list(ecg_table['delta_age'])
code_blood_table = list(ecg_table['code_blood_table'])
parameters_names = list(ecg_table.columns)[12:]

result_path = path + '/correlation_groups/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

metrics_dict_age = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': []}

subjects_ids = list(range(0, len(ages)))
pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, subjects_ids,
                                                            metrics_dict_age, metrics_dict_delta)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age)
metrics_dict_age['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age)
metrics_dict_age['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age, result_path, 'correlation_age')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta)
metrics_dict_delta['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta)
metrics_dict_delta['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta, result_path, 'correlation_delta_age')

# Correlation for Down subjects
metrics_dict_age_down = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_down = {'param': [], 'spearman_rho': [], 'spearman_pval': [], 'pearson_coef': [], 'pearson_pval': []}

down_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        down_ids.append(i)

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, down_ids,
                                                            metrics_dict_age_down, metrics_dict_delta_down)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_down)
metrics_dict_age_down['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_down)
metrics_dict_age_down['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down, result_path, 'correlation_age_down')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_down)
metrics_dict_delta_down['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_down)
metrics_dict_delta_down['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down, result_path, 'correlation_delta_age_down')
