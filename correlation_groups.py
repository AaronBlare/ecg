import os
import pandas as pd
from path import get_path
from functions import calculate_correlation_with_age, calculate_correlation_with_sex, multiple_test_correction
from save import save_dict_to_xlsx

path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ages = list(ecg_table['age'])
ph_ages = list(ecg_table['phenotypic_age'])
delta_ages = list(ecg_table['delta_age'])
sexes = list(ecg_table['sex'])
code_blood_table = list(ecg_table['code_blood_table'])
parameters_names = list(ecg_table.columns)[12:]

result_path = path + '/correlation_groups/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

metrics_dict_age_spearman = {'param': []}
metrics_dict_ph_age_spearman = {'param': []}
metrics_dict_delta_age_spearman = {'param': []}

# Correlation for all subjects with age and delta age
metrics_dict_age = {'param': [],
                    'spearman_rho': [], 'spearman_pval': [],
                    'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age = {'param': [],
                       'spearman_rho': [], 'spearman_pval': [],
                       'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta = {'param': [],
                      'spearman_rho': [], 'spearman_pval': [],
                      'pearson_coef': [], 'pearson_pval': []}

subjects_ids = list(range(0, len(ages)))
pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, subjects_ids, metrics_dict_age,
                                                                          metrics_dict_ph_age, metrics_dict_delta)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age)
metrics_dict_age['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age)
metrics_dict_age['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age, result_path, 'correlation_age')
metrics_dict_age_spearman['param'] = metrics_dict_age['param']
metrics_dict_age_spearman['all'] = metrics_dict_age['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age)
metrics_dict_ph_age['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age)
metrics_dict_ph_age['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age, result_path, 'correlation_ph_age')
metrics_dict_ph_age_spearman['param'] = metrics_dict_ph_age['param']
metrics_dict_ph_age_spearman['all'] = metrics_dict_ph_age['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta)
metrics_dict_delta['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta)
metrics_dict_delta['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta, result_path, 'correlation_delta_age')
metrics_dict_delta_age_spearman['param'] = metrics_dict_delta['param']
metrics_dict_delta_age_spearman['all'] = metrics_dict_delta['spearman_rho']

# Correlation for Down subjects with age and delta age
metrics_dict_age_down = {'param': [],
                         'spearman_rho': [], 'spearman_pval': [],
                         'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_down = {'param': [],
                            'spearman_rho': [], 'spearman_pval': [],
                            'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_down = {'param': [],
                           'spearman_rho': [], 'spearman_pval': [],
                           'pearson_coef': [], 'pearson_pval': []}

down_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        down_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, down_ids, metrics_dict_age_down,
                                                                          metrics_dict_ph_age_down,
                                                                          metrics_dict_delta_down)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_down)
metrics_dict_age_down['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_down)
metrics_dict_age_down['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down, result_path, 'correlation_age_down')
metrics_dict_age_spearman['down'] = metrics_dict_age_down['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_down)
metrics_dict_ph_age_down['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_down)
metrics_dict_ph_age_down['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_down, result_path, 'correlation_ph_age_down')
metrics_dict_ph_age_spearman['down'] = metrics_dict_ph_age_down['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_down)
metrics_dict_delta_down['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_down)
metrics_dict_delta_down['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down, result_path, 'correlation_delta_age_down')
metrics_dict_delta_age_spearman['down'] = metrics_dict_delta_down['spearman_rho']

# Correlation for Down siblings with age and delta age
metrics_dict_age_down_sibling = {'param': [],
                                 'spearman_rho': [], 'spearman_pval': [],
                                 'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_down_sibling = {'param': [],
                                    'spearman_rho': [], 'spearman_pval': [],
                                    'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_down_sibling = {'param': [],
                                   'spearman_rho': [], 'spearman_pval': [],
                                   'pearson_coef': [], 'pearson_pval': []}

down_siblings_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('B') or str(code).startswith('S'):
        if 'Q' in str(code):
            down_siblings_ids.append(i)

pvals_age, pvals_ph, pvals_delta_age = calculate_correlation_with_age(ecg_table, down_siblings_ids,
                                                                      metrics_dict_age_down_sibling,
                                                                      metrics_dict_ph_age_down_sibling,
                                                                      metrics_dict_delta_down_sibling)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_down_sibling)
metrics_dict_age_down_sibling['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_down_sibling)
metrics_dict_age_down_sibling['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down_sibling, result_path, 'correlation_age_down_sibling')
metrics_dict_age_spearman['down_sibling'] = metrics_dict_age_down_sibling['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_down_sibling)
metrics_dict_ph_age_down_sibling['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_down_sibling)
metrics_dict_ph_age_down_sibling['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_down_sibling, result_path, 'correlation_ph_age_down_sibling')
metrics_dict_ph_age_spearman['down_sibling'] = metrics_dict_ph_age_down_sibling['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_down_sibling)
metrics_dict_delta_down_sibling['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_down_sibling)
metrics_dict_delta_down_sibling['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down_sibling, result_path, 'correlation_delta_age_down_sibling')
metrics_dict_delta_age_spearman['down_sibling'] = metrics_dict_delta_down_sibling['spearman_rho']

# Correlation for Down parents with age and delta age
metrics_dict_age_down_parent = {'param': [],
                                'spearman_rho': [], 'spearman_pval': [],
                                'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_down_parent = {'param': [],
                                   'spearman_rho': [], 'spearman_pval': [],
                                   'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_down_parent = {'param': [],
                                  'spearman_rho': [], 'spearman_pval': [],
                                  'pearson_coef': [], 'pearson_pval': []}

down_parent_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('F') or str(code).startswith('M'):
        if 'Q' in str(code):
            down_parent_ids.append(i)

pvals_age, pvals_ph, pvals_delta_age = calculate_correlation_with_age(ecg_table, down_parent_ids,
                                                                      metrics_dict_age_down_parent,
                                                                      metrics_dict_ph_age_down_parent,
                                                                      metrics_dict_delta_down_parent)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_down_parent)
metrics_dict_age_down_parent['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_down_parent)
metrics_dict_age_down_parent['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down_parent, result_path, 'correlation_age_down_parent')
metrics_dict_age_spearman['down_parent'] = metrics_dict_age_down_parent['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_down_parent)
metrics_dict_ph_age_down_parent['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_down_parent)
metrics_dict_ph_age_down_parent['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_down_parent, result_path, 'correlation_ph_age_down_parent')
metrics_dict_ph_age_spearman['down_parent'] = metrics_dict_ph_age_down_parent['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_down_parent)
metrics_dict_delta_down_parent['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_down_parent)
metrics_dict_delta_down_parent['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down_parent, result_path, 'correlation_delta_age_down_parent')
metrics_dict_delta_age_spearman['down_parent'] = metrics_dict_delta_down_parent['spearman_rho']

# Correlation for long-living subjects with age and delta age
metrics_dict_age_long_living = {'param': [],
                                'spearman_rho': [], 'spearman_pval': [],
                                'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_long_living = {'param': [],
                                   'spearman_rho': [], 'spearman_pval': [],
                                   'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_long_living = {'param': [],
                                  'spearman_rho': [], 'spearman_pval': [],
                                  'pearson_coef': [], 'pearson_pval': []}

long_living_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('L'):
        long_living_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, long_living_ids,
                                                                          metrics_dict_age_long_living,
                                                                          metrics_dict_ph_age_long_living,
                                                                          metrics_dict_delta_long_living)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_long_living)
metrics_dict_age_long_living['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_long_living)
metrics_dict_age_long_living['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_long_living, result_path, 'correlation_age_long_living')
metrics_dict_age_spearman['long_living'] = metrics_dict_age_long_living['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_long_living)
metrics_dict_ph_age_long_living['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_long_living)
metrics_dict_ph_age_long_living['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_long_living, result_path, 'correlation_ph_age_long_living')
metrics_dict_ph_age_spearman['long_living'] = metrics_dict_ph_age_long_living['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_long_living)
metrics_dict_delta_long_living['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_long_living)
metrics_dict_delta_long_living['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_long_living, result_path, 'correlation_delta_age_long_living')
metrics_dict_delta_age_spearman['long_living'] = metrics_dict_delta_long_living['spearman_rho']

# Correlation for long-living subjects family with age and delta age
metrics_dict_age_long_living_family = {'param': [],
                                       'spearman_rho': [], 'spearman_pval': [],
                                       'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_long_living_family = {'param': [],
                                          'spearman_rho': [], 'spearman_pval': [],
                                          'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_long_living_family = {'param': [],
                                         'spearman_rho': [], 'spearman_pval': [],
                                         'pearson_coef': [], 'pearson_pval': []}

long_living_family_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('F'):
        if 'L' in str(code):
            long_living_family_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, long_living_family_ids,
                                                                          metrics_dict_age_long_living_family,
                                                                          metrics_dict_ph_age_long_living_family,
                                                                          metrics_dict_delta_long_living_family)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_long_living_family)
metrics_dict_age_long_living_family['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_long_living_family)
metrics_dict_age_long_living_family['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_long_living_family, result_path, 'correlation_age_long_living_family')
metrics_dict_age_spearman['long_living_family'] = metrics_dict_age_long_living_family['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_long_living_family)
metrics_dict_ph_age_long_living_family['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni',
                                                      metrics_dict_ph_age_long_living_family)
metrics_dict_ph_age_long_living_family['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_long_living_family, result_path, 'correlation_ph_age_long_living_family')
metrics_dict_ph_age_spearman['long_living_family'] = metrics_dict_ph_age_long_living_family['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_long_living_family)
metrics_dict_delta_long_living_family['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_long_living_family)
metrics_dict_delta_long_living_family['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_long_living_family, result_path, 'correlation_delta_age_long_living_family')
metrics_dict_delta_age_spearman['long_living_family'] = metrics_dict_delta_long_living_family['spearman_rho']

# Correlation for stressed subjects with age and delta age
metrics_dict_age_stress = {'param': [],
                           'spearman_rho': [], 'spearman_pval': [],
                           'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_stress = {'param': [],
                              'spearman_rho': [], 'spearman_pval': [],
                              'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_stress = {'param': [],
                             'spearman_rho': [], 'spearman_pval': [],
                             'pearson_coef': [], 'pearson_pval': []}

stress_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('S'):
        if 'L' not in str(code) and 'Q' not in str(code):
            stress_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, stress_ids,
                                                                          metrics_dict_age_stress,
                                                                          metrics_dict_ph_age_stress,
                                                                          metrics_dict_delta_stress)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_stress)
metrics_dict_age_stress['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_stress)
metrics_dict_age_stress['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_stress, result_path, 'correlation_age_stress')
metrics_dict_age_spearman['stress'] = metrics_dict_age_stress['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_stress)
metrics_dict_ph_age_stress['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_stress)
metrics_dict_ph_age_stress['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_stress, result_path, 'correlation_ph_age_stress')
metrics_dict_ph_age_spearman['stress'] = metrics_dict_ph_age_stress['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_stress)
metrics_dict_delta_stress['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_stress)
metrics_dict_delta_stress['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_stress, result_path, 'correlation_delta_age_stress')
metrics_dict_delta_age_spearman['stress'] = metrics_dict_delta_stress['spearman_rho']

# Correlation for control subjects with age and delta age
metrics_dict_age_control = {'param': [],
                            'spearman_rho': [], 'spearman_pval': [],
                            'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_control = {'param': [],
                               'spearman_rho': [], 'spearman_pval': [],
                               'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_control = {'param': [],
                              'spearman_rho': [], 'spearman_pval': [],
                              'pearson_coef': [], 'pearson_pval': []}

control_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('I'):
        control_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, control_ids,
                                                                          metrics_dict_age_control,
                                                                          metrics_dict_ph_age_control,
                                                                          metrics_dict_delta_control)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_control)
metrics_dict_age_control['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_control)
metrics_dict_age_control['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_control, result_path, 'correlation_age_control')
metrics_dict_age_spearman['control'] = metrics_dict_age_control['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_control)
metrics_dict_ph_age_control['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_control)
metrics_dict_ph_age_control['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_control, result_path, 'correlation_ph_age_control')
metrics_dict_ph_age_spearman['control'] = metrics_dict_ph_age_control['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_control)
metrics_dict_delta_control['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_control)
metrics_dict_delta_control['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_control, result_path, 'correlation_delta_age_control')
metrics_dict_delta_age_spearman['control'] = metrics_dict_delta_control['spearman_rho']

# Correlation for anemia subjects with age and delta age
metrics_dict_age_anemia = {'param': [],
                           'spearman_rho': [], 'spearman_pval': [],
                           'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_anemia = {'param': [],
                              'spearman_rho': [], 'spearman_pval': [],
                              'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_anemia = {'param': [],
                             'spearman_rho': [], 'spearman_pval': [],
                             'pearson_coef': [], 'pearson_pval': []}

anemia_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('A'):
        anemia_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, anemia_ids,
                                                                          metrics_dict_age_anemia,
                                                                          metrics_dict_ph_age_anemia,
                                                                          metrics_dict_delta_anemia)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_anemia)
metrics_dict_age_anemia['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_anemia)
metrics_dict_age_anemia['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_anemia, result_path, 'correlation_age_anemia')
metrics_dict_age_spearman['anemia'] = metrics_dict_age_anemia['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_anemia)
metrics_dict_ph_age_anemia['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_anemia)
metrics_dict_ph_age_anemia['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_anemia, result_path, 'correlation_ph_age_anemia')
metrics_dict_ph_age_spearman['anemia'] = metrics_dict_ph_age_anemia['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_anemia)
metrics_dict_delta_anemia['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_anemia)
metrics_dict_delta_anemia['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_anemia, result_path, 'correlation_delta_age_anemia')
metrics_dict_delta_age_spearman['anemia'] = metrics_dict_delta_anemia['spearman_rho']

# Correlation for hemodialysis subjects with age and delta age
metrics_dict_age_dialysis = {'param': [],
                             'spearman_rho': [], 'spearman_pval': [],
                             'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_dialysis = {'param': [],
                                'spearman_rho': [], 'spearman_pval': [],
                                'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_dialysis = {'param': [],
                               'spearman_rho': [], 'spearman_pval': [],
                               'pearson_coef': [], 'pearson_pval': []}

dialysis_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('H'):
        dialysis_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, dialysis_ids,
                                                                          metrics_dict_age_dialysis,
                                                                          metrics_dict_ph_age_dialysis,
                                                                          metrics_dict_delta_dialysis)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_dialysis)
metrics_dict_age_dialysis['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_dialysis)
metrics_dict_age_dialysis['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_dialysis, result_path, 'correlation_age_dialysis')
metrics_dict_age_spearman['dialysis'] = metrics_dict_age_dialysis['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_dialysis)
metrics_dict_ph_age_dialysis['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_dialysis)
metrics_dict_ph_age_dialysis['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_dialysis, result_path, 'correlation_ph_age_dialysis')
metrics_dict_ph_age_spearman['dialysis'] = metrics_dict_ph_age_dialysis['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_dialysis)
metrics_dict_delta_dialysis['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_dialysis)
metrics_dict_delta_dialysis['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_dialysis, result_path, 'correlation_delta_age_dialysis')
metrics_dict_delta_age_spearman['dialysis'] = metrics_dict_delta_dialysis['spearman_rho']

# Correlation for healthy (stress and control) subjects with age and delta age
metrics_dict_age_healthy = {'param': [],
                            'spearman_rho': [], 'spearman_pval': [],
                            'pearson_coef': [], 'pearson_pval': []}
metrics_dict_ph_age_healthy = {'param': [],
                               'spearman_rho': [], 'spearman_pval': [],
                               'pearson_coef': [], 'pearson_pval': []}
metrics_dict_delta_healthy = {'param': [],
                              'spearman_rho': [], 'spearman_pval': [],
                              'pearson_coef': [], 'pearson_pval': []}

healthy_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('S'):
        if 'L' not in str(code) and 'Q' not in str(code):
            healthy_ids.append(i)
    elif str(code).startswith('I'):
        healthy_ids.append(i)

pvals_age, pvals_ph_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, healthy_ids,
                                                                          metrics_dict_age_healthy,
                                                                          metrics_dict_ph_age_healthy,
                                                                          metrics_dict_delta_healthy)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_healthy)
metrics_dict_age_healthy['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_healthy)
metrics_dict_age_healthy['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_healthy, result_path, 'correlation_age_healthy')
metrics_dict_age_spearman['healthy'] = metrics_dict_age_healthy['spearman_rho']

pval_ph_age_corrected_bh = multiple_test_correction(pvals_ph_age, 'fdr_bh', metrics_dict_ph_age_healthy)
metrics_dict_ph_age_healthy['spearman_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals_ph_age, 'bonferroni', metrics_dict_ph_age_healthy)
metrics_dict_ph_age_healthy['spearman_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_healthy, result_path, 'correlation_ph_age_healthy')
metrics_dict_ph_age_spearman['healthy'] = metrics_dict_ph_age_healthy['spearman_rho']

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_healthy)
metrics_dict_delta_healthy['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_healthy)
metrics_dict_delta_healthy['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_healthy, result_path, 'correlation_delta_age_healthy')
metrics_dict_delta_age_spearman['healthy'] = metrics_dict_delta_healthy['spearman_rho']

save_dict_to_xlsx(metrics_dict_age_spearman, result_path, 'correlation_age_spearman')
save_dict_to_xlsx(metrics_dict_ph_age_spearman, result_path, 'correlation_ph_age_spearman')
save_dict_to_xlsx(metrics_dict_delta_age_spearman, result_path, 'correlation_delta_age_spearman')

####################################################################################################################

metrics_dict_sex_point_biserial = {'param': []}

# Correlation for all subjects with sex
metrics_dict_sex = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

subjects_ids = list(range(0, len(sexes)))
pvals_sex = calculate_correlation_with_sex(ecg_table, subjects_ids, metrics_dict_sex)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex)
metrics_dict_sex['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex)
metrics_dict_sex['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex, result_path, 'correlation_sex')
metrics_dict_sex_point_biserial['param'] = metrics_dict_sex['param']
metrics_dict_sex_point_biserial['all'] = metrics_dict_sex['point_biserial_coeff']

# Correlation for Down subjects with sex
metrics_dict_sex_down = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

down_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        down_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, down_ids, metrics_dict_sex_down)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_down)
metrics_dict_sex_down['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_down)
metrics_dict_sex_down['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_down, result_path, 'correlation_sex_down')
metrics_dict_sex_point_biserial['down'] = metrics_dict_sex_down['point_biserial_coeff']

# Correlation for Down siblings with sex
metrics_dict_sex_down_sibling = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

down_siblings_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('B') or str(code).startswith('S'):
        if 'Q' in str(code):
            down_siblings_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, down_siblings_ids, metrics_dict_sex_down_sibling)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_down_sibling)
metrics_dict_sex_down_sibling['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_down_sibling)
metrics_dict_sex_down_sibling['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_down_sibling, result_path, 'correlation_sex_down_sibling')
metrics_dict_sex_point_biserial['down_sibling'] = metrics_dict_sex_down_sibling['point_biserial_coeff']

# Correlation for Down parents with sex
metrics_dict_sex_down_parent = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

down_parent_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('F') or str(code).startswith('M'):
        if 'Q' in str(code):
            down_parent_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, down_parent_ids, metrics_dict_sex_down_parent)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_down_parent)
metrics_dict_sex_down_parent['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_down_parent)
metrics_dict_sex_down_parent['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_down_parent, result_path, 'correlation_sex_down_parent')
metrics_dict_sex_point_biserial['down_parent'] = metrics_dict_sex_down_parent['point_biserial_coeff']

# Correlation for long-living subjects with sex
metrics_dict_sex_long_living = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

long_living_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('L'):
        long_living_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, long_living_ids, metrics_dict_sex_long_living)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_long_living)
metrics_dict_sex_long_living['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_long_living)
metrics_dict_sex_long_living['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_long_living, result_path, 'correlation_sex_long_living')
metrics_dict_sex_point_biserial['long_living'] = metrics_dict_sex_long_living['point_biserial_coeff']

# Correlation for stressed subjects with sex
metrics_dict_sex_stress = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

stress_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('S'):
        if 'L' not in str(code) and 'Q' not in str(code):
            stress_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, stress_ids, metrics_dict_sex_stress)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_stress)
metrics_dict_sex_stress['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_stress)
metrics_dict_sex_stress['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_stress, result_path, 'correlation_sex_stress')
metrics_dict_sex_point_biserial['stress'] = metrics_dict_sex_stress['point_biserial_coeff']

# Correlation for control subjects with sex
metrics_dict_sex_control = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

control_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('I'):
        control_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, control_ids, metrics_dict_sex_control)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_control)
metrics_dict_sex_control['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_control)
metrics_dict_sex_control['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_control, result_path, 'correlation_sex_control')
metrics_dict_sex_point_biserial['control'] = metrics_dict_sex_control['point_biserial_coeff']

# Correlation for hemodialysis subjects with sex
metrics_dict_sex_dialysis = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

dialysis_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('H'):
        dialysis_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, dialysis_ids, metrics_dict_sex_dialysis)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_dialysis)
metrics_dict_sex_dialysis['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_dialysis)
metrics_dict_sex_dialysis['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_dialysis, result_path, 'correlation_sex_dialysis')
metrics_dict_sex_point_biserial['dialysis'] = metrics_dict_sex_dialysis['point_biserial_coeff']

# Correlation for healthy (stress and control) subjects with sex
metrics_dict_sex_healthy = {'param': [], 'point_biserial_coeff': [], 'point_biserial_pval': []}

healthy_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('S'):
        if 'L' not in str(code) and 'Q' not in str(code):
            healthy_ids.append(i)
    elif str(code).startswith('I'):
        healthy_ids.append(i)

pvals_sex = calculate_correlation_with_sex(ecg_table, healthy_ids, metrics_dict_sex_healthy)

pval_sex_corrected_bh = multiple_test_correction(pvals_sex, 'fdr_bh', metrics_dict_sex_healthy)
metrics_dict_sex_healthy['point_biserial_pval_corr_bh'] = pval_sex_corrected_bh
pval_sex_corrected_bonf = multiple_test_correction(pvals_sex, 'bonferroni', metrics_dict_sex_healthy)
metrics_dict_sex_healthy['point_biserial_pval_corr_bonf'] = pval_sex_corrected_bonf

save_dict_to_xlsx(metrics_dict_sex_healthy, result_path, 'correlation_sex_healthy')
metrics_dict_sex_point_biserial['healthy'] = metrics_dict_sex_healthy['point_biserial_coeff']

save_dict_to_xlsx(metrics_dict_sex_point_biserial, result_path, 'correlation_sex_point_biserial')
