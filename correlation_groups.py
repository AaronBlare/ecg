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

# Correlation for all subjects with age and delta age
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

# Correlation for Down subjects with age and delta age
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

# Correlation for Down siblings with age and delta age
metrics_dict_age_down_sibling = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, down_siblings_ids,
                                                            metrics_dict_age_down_sibling,
                                                            metrics_dict_delta_down_sibling)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_down_sibling)
metrics_dict_age_down_sibling['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_down_sibling)
metrics_dict_age_down_sibling['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down_sibling, result_path, 'correlation_age_down_sibling')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_down_sibling)
metrics_dict_delta_down_sibling['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_down_sibling)
metrics_dict_delta_down_sibling['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down_sibling, result_path, 'correlation_delta_age_down_sibling')

# Correlation for Down parents with age and delta age
metrics_dict_age_down_parent = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, down_parent_ids,
                                                            metrics_dict_age_down_parent,
                                                            metrics_dict_delta_down_parent)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_down_parent)
metrics_dict_age_down_parent['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_down_parent)
metrics_dict_age_down_parent['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down_parent, result_path, 'correlation_age_down_parent')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_down_parent)
metrics_dict_delta_down_parent['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_down_parent)
metrics_dict_delta_down_parent['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down_parent, result_path, 'correlation_delta_age_down_parent')

# Correlation for long-living subjects with age and delta age
metrics_dict_age_long_living = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, long_living_ids,
                                                            metrics_dict_age_long_living,
                                                            metrics_dict_delta_long_living)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_long_living)
metrics_dict_age_long_living['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_long_living)
metrics_dict_age_long_living['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_long_living, result_path, 'correlation_age_long_living')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_long_living)
metrics_dict_delta_long_living['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni', metrics_dict_delta_long_living)
metrics_dict_delta_long_living['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_long_living, result_path, 'correlation_delta_age_long_living')

# Correlation for long-living subjects family with age and delta age
metrics_dict_age_long_living_family = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, long_living_family_ids,
                                                            metrics_dict_age_long_living_family,
                                                            metrics_dict_delta_long_living_family)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_long_living_family)
metrics_dict_age_long_living_family['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_long_living_family)
metrics_dict_age_long_living_family['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_long_living_family, result_path, 'correlation_age_long_living_family')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_long_living_family)
metrics_dict_delta_long_living_family['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_long_living_family)
metrics_dict_delta_long_living_family['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_long_living_family, result_path, 'correlation_delta_age_long_living_family')

# Correlation for stressed subjects with age and delta age
metrics_dict_age_stress = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, stress_ids,
                                                            metrics_dict_age_stress,
                                                            metrics_dict_delta_stress)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_stress)
metrics_dict_age_stress['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_stress)
metrics_dict_age_stress['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_stress, result_path, 'correlation_age_stress')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_stress)
metrics_dict_delta_stress['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_stress)
metrics_dict_delta_stress['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_stress, result_path, 'correlation_delta_age_stress')

# Correlation for control subjects with age and delta age
metrics_dict_age_control = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, control_ids,
                                                            metrics_dict_age_control,
                                                            metrics_dict_delta_control)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_control)
metrics_dict_age_control['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_control)
metrics_dict_age_control['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_control, result_path, 'correlation_age_control')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_control)
metrics_dict_delta_control['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_control)
metrics_dict_delta_control['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_control, result_path, 'correlation_delta_age_control')

# Correlation for anemia subjects with age and delta age
metrics_dict_age_anemia = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, anemia_ids,
                                                            metrics_dict_age_anemia,
                                                            metrics_dict_delta_anemia)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_anemia)
metrics_dict_age_anemia['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_anemia)
metrics_dict_age_anemia['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_anemia, result_path, 'correlation_age_anemia')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_anemia)
metrics_dict_delta_anemia['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_anemia)
metrics_dict_delta_anemia['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_anemia, result_path, 'correlation_delta_age_anemia')

# Correlation for hemodialysis subjects with age and delta age
metrics_dict_age_dialysis = {'param': [],
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

pvals_age, pvals_delta_age = calculate_correlation_with_age(ecg_table, dialysis_ids,
                                                            metrics_dict_age_dialysis,
                                                            metrics_dict_delta_dialysis)

pval_age_corrected_bh = multiple_test_correction(pvals_age, 'fdr_bh', metrics_dict_age_dialysis)
metrics_dict_age_dialysis['spearman_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals_age, 'bonferroni', metrics_dict_age_dialysis)
metrics_dict_age_dialysis['spearman_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_dialysis, result_path, 'correlation_age_dialysis')

pval_delta_corrected_bh = multiple_test_correction(pvals_delta_age, 'fdr_bh', metrics_dict_delta_dialysis)
metrics_dict_delta_dialysis['spearman_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals_delta_age, 'bonferroni',
                                                     metrics_dict_delta_dialysis)
metrics_dict_delta_dialysis['spearman_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_dialysis, result_path, 'correlation_delta_age_dialysis')
