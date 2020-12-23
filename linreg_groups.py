import os
import pandas as pd
from path import get_path
from functions import build_linreg_with_age, multiple_test_correction
from save import save_dict_to_xlsx

path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ages = list(ecg_table['age'])
ph_ages = list(ecg_table['phenotypic_age'])
delta_ages = list(ecg_table['delta_age'])
code_blood_table = list(ecg_table['code_blood_table'])
parameters_names = list(ecg_table.columns)[12:]

result_path = path + '/linreg_groups/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

metrics_dict_age_linreg = {'param': []}
metrics_dict_ph_age_linreg = {'param': []}
metrics_dict_delta_age_linreg = {'param': []}

# Linear regression for all subjects with age and delta age
metrics_dict_age = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [], 'slope_std': [],
                    'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [], 'slope_std': [],
                       'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [], 'slope_std': [],
                      'intercept_p_value': [], 'slope_p_value': []}

subjects_ids = list(range(0, len(ages)))
pvals_age, pvals_ph_age, pvals_delta_age = build_linreg_with_age(ecg_table, subjects_ids, metrics_dict_age,
                                                                 metrics_dict_ph_age, metrics_dict_delta)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age)
metrics_dict_age['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age)
metrics_dict_age['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age, result_path, 'linreg_age')
metrics_dict_age_linreg['param'] = metrics_dict_age['param']
metrics_dict_age_linreg['all'] = metrics_dict_age['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age)
metrics_dict_ph_age['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age)
metrics_dict_ph_age['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age, result_path, 'linreg_ph_age')
metrics_dict_age_linreg['param'] = metrics_dict_ph_age['param']
metrics_dict_age_linreg['all'] = metrics_dict_ph_age['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta)
metrics_dict_delta['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta)
metrics_dict_delta['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta, result_path, 'linreg_delta_age')
metrics_dict_age_linreg['param'] = metrics_dict_delta['param']
metrics_dict_age_linreg['all'] = metrics_dict_delta['R2']
