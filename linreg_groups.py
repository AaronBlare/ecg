import os
import pandas as pd
from path import get_path
from functions import build_linreg_with_age, plot_linreg, multiple_test_correction
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

plot_path = path + '/linreg_groups/plot/'
if not os.path.exists(plot_path):
    os.makedirs(plot_path)

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
pvals = build_linreg_with_age(ecg_table, subjects_ids, metrics_dict_age, metrics_dict_ph_age, metrics_dict_delta)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age)
metrics_dict_age['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age)
metrics_dict_age['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age, result_path, 'linreg_age')
plot_linreg(ecg_table, subjects_ids, metrics_dict_age, 'age', 'all', plot_path)
metrics_dict_age_linreg['param'] = metrics_dict_age['param']
metrics_dict_age_linreg['all'] = metrics_dict_age['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age)
metrics_dict_ph_age['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age)
metrics_dict_ph_age['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age, result_path, 'linreg_ph_age')
plot_linreg(ecg_table, subjects_ids, metrics_dict_ph_age, 'ph_age', 'all', plot_path)
metrics_dict_ph_age_linreg['param'] = metrics_dict_ph_age['param']
metrics_dict_ph_age_linreg['all'] = metrics_dict_ph_age['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta)
metrics_dict_delta['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta)
metrics_dict_delta['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta, result_path, 'linreg_delta_age')
plot_linreg(ecg_table, subjects_ids, metrics_dict_delta, 'delta_age', 'all', plot_path)
metrics_dict_delta_age_linreg['param'] = metrics_dict_delta['param']
metrics_dict_delta_age_linreg['all'] = metrics_dict_delta['R2']

# Correlation for Down subjects with age and delta age
metrics_dict_age_down = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [], 'slope_std': [],
                         'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_down = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [], 'slope_std': [],
                            'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_down = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [], 'slope_std': [],
                           'intercept_p_value': [], 'slope_p_value': []}

down_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('Q'):
        down_ids.append(i)

pvals = build_linreg_with_age(ecg_table, down_ids, metrics_dict_age_down, metrics_dict_ph_age_down,
                              metrics_dict_delta_down)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_down)
metrics_dict_age_down['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_down)
metrics_dict_age_down['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down, result_path, 'linreg_age_down')
plot_linreg(ecg_table, down_ids, metrics_dict_age_down, 'age', 'down', plot_path)
metrics_dict_age_linreg['down'] = metrics_dict_age_down['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_down)
metrics_dict_ph_age_down['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_down)
metrics_dict_ph_age_down['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_down, result_path, 'linreg_ph_age_down')
plot_linreg(ecg_table, down_ids, metrics_dict_ph_age_down, 'ph_age', 'down', plot_path)
metrics_dict_ph_age_linreg['down'] = metrics_dict_ph_age_down['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_down)
metrics_dict_delta_down['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_down)
metrics_dict_delta_down['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down, result_path, 'linreg_delta_age_down')
plot_linreg(ecg_table, down_ids, metrics_dict_delta_down, 'delta_age', 'down', plot_path)
metrics_dict_delta_age_linreg['down'] = metrics_dict_delta_down['R2']

# Correlation for Down siblings with age and delta age
metrics_dict_age_down_sibling = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                 'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_down_sibling = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                    'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_down_sibling = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                   'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

down_siblings_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('B') or str(code).startswith('S'):
        if 'Q' in str(code):
            down_siblings_ids.append(i)

pvals = build_linreg_with_age(ecg_table, down_siblings_ids, metrics_dict_age_down_sibling,
                              metrics_dict_ph_age_down_sibling, metrics_dict_delta_down_sibling)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_down_sibling)
metrics_dict_age_down_sibling['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_down_sibling)
metrics_dict_age_down_sibling['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down_sibling, result_path, 'linreg_age_down_sibling')
plot_linreg(ecg_table, down_siblings_ids, metrics_dict_age_down_sibling, 'age', 'down_sibling', plot_path)
metrics_dict_age_linreg['down_sibling'] = metrics_dict_age_down_sibling['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_down_sibling)
metrics_dict_ph_age_down_sibling['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_down_sibling)
metrics_dict_ph_age_down_sibling['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_down_sibling, result_path, 'linreg_ph_age_down_sibling')
plot_linreg(ecg_table, down_siblings_ids, metrics_dict_ph_age_down_sibling, 'ph_age', 'down_sibling',
            plot_path)
metrics_dict_ph_age_linreg['down_sibling'] = metrics_dict_ph_age_down_sibling['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_down_sibling)
metrics_dict_delta_down_sibling['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_down_sibling)
metrics_dict_delta_down_sibling['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down_sibling, result_path, 'linreg_delta_age_down_sibling')
plot_linreg(ecg_table, down_siblings_ids, metrics_dict_delta_down_sibling, 'delta_age', 'down_sibling', plot_path)
metrics_dict_delta_age_linreg['down_sibling'] = metrics_dict_delta_down_sibling['R2']

# Correlation for Down parents with age and delta age
metrics_dict_age_down_parent = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_down_parent = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                   'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_down_parent = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                  'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

down_parent_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('F') or str(code).startswith('M'):
        if 'Q' in str(code):
            down_parent_ids.append(i)

pvals = build_linreg_with_age(ecg_table, down_parent_ids, metrics_dict_age_down_parent, metrics_dict_ph_age_down_parent,
                              metrics_dict_delta_down_parent)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_down_parent)
metrics_dict_age_down_parent['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_down_parent)
metrics_dict_age_down_parent['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_down_parent, result_path, 'linreg_age_down_parent')
plot_linreg(ecg_table, down_parent_ids, metrics_dict_age_down_parent, 'age', 'down_parent', plot_path)
metrics_dict_age_linreg['down_parent'] = metrics_dict_age_down_parent['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_down_parent)
metrics_dict_ph_age_down_parent['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_down_parent)
metrics_dict_ph_age_down_parent['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_down_parent, result_path, 'linreg_ph_age_down_parent')
plot_linreg(ecg_table, down_parent_ids, metrics_dict_ph_age_down_parent, 'ph_age', 'down_parent', plot_path)
metrics_dict_ph_age_linreg['down_parent'] = metrics_dict_ph_age_down_parent['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_down_parent)
metrics_dict_delta_down_parent['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_down_parent)
metrics_dict_delta_down_parent['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_down_parent, result_path, 'linreg_delta_age_down_parent')
plot_linreg(ecg_table, down_parent_ids, metrics_dict_delta_down_parent, 'delta_age', 'down_parent', plot_path)
metrics_dict_delta_age_linreg['down_parent'] = metrics_dict_delta_down_parent['R2']

# Correlation for long-living subjects with age and delta age
metrics_dict_age_long_living = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_long_living = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                   'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_long_living = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                  'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

long_living_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('L'):
        long_living_ids.append(i)

pvals = build_linreg_with_age(ecg_table, long_living_ids, metrics_dict_age_long_living, metrics_dict_ph_age_long_living,
                              metrics_dict_delta_long_living)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_long_living)
metrics_dict_age_long_living['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_long_living)
metrics_dict_age_long_living['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_long_living, result_path, 'linreg_age_long_living')
plot_linreg(ecg_table, long_living_ids, metrics_dict_delta_down_parent, 'age', 'long_living', plot_path)
metrics_dict_age_linreg['long_living'] = metrics_dict_age_long_living['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_long_living)
metrics_dict_ph_age_long_living['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_long_living)
metrics_dict_ph_age_long_living['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_long_living, result_path, 'linreg_ph_age_long_living')
plot_linreg(ecg_table, long_living_ids, metrics_dict_ph_age_long_living, 'ph_age', 'long_living', plot_path)
metrics_dict_ph_age_linreg['long_living'] = metrics_dict_ph_age_long_living['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_long_living)
metrics_dict_delta_long_living['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_long_living)
metrics_dict_delta_long_living['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_long_living, result_path, 'linreg_delta_age_long_living')
plot_linreg(ecg_table, long_living_ids, metrics_dict_delta_long_living, 'delta_age', 'long_living', plot_path)
metrics_dict_delta_age_linreg['long_living'] = metrics_dict_delta_long_living['R2']

# Correlation for long-living subjects family with age and delta age
metrics_dict_age_long_living_family = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                       'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_long_living_family = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                          'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_long_living_family = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                         'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

long_living_family_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('F'):
        if 'L' in str(code):
            long_living_family_ids.append(i)

pvals = build_linreg_with_age(ecg_table, long_living_family_ids, metrics_dict_age_long_living_family,
                              metrics_dict_ph_age_long_living_family, metrics_dict_delta_long_living_family)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_long_living_family)
metrics_dict_age_long_living_family['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_long_living_family)
metrics_dict_age_long_living_family['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_long_living_family, result_path, 'linreg_age_long_living_family')
plot_linreg(ecg_table, long_living_family_ids, metrics_dict_age_long_living_family, 'age', 'long_living_family',
            plot_path)
metrics_dict_age_linreg['long_living_family'] = metrics_dict_age_long_living_family['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_long_living_family)
metrics_dict_ph_age_long_living_family['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni',
                                                      metrics_dict_ph_age_long_living_family)
metrics_dict_ph_age_long_living_family['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_long_living_family, result_path, 'linreg_ph_age_long_living_family')
plot_linreg(ecg_table, long_living_family_ids, metrics_dict_ph_age_long_living_family, 'ph_age', 'long_living_family',
            plot_path)
metrics_dict_ph_age_linreg['long_living_family'] = metrics_dict_ph_age_long_living_family['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_long_living_family)
metrics_dict_delta_long_living_family['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni',
                                                     metrics_dict_delta_long_living_family)
metrics_dict_delta_long_living_family['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_long_living_family, result_path, 'linreg_delta_age_long_living_family')
plot_linreg(ecg_table, long_living_family_ids, metrics_dict_delta_long_living_family, 'delta_age', 'long_living_family',
            plot_path)
metrics_dict_delta_age_linreg['long_living_family'] = metrics_dict_delta_long_living_family['R2']

# Correlation for stressed subjects with age and delta age
metrics_dict_age_stress = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                           'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_stress = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                              'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_stress = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                             'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

stress_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('S'):
        if 'L' not in str(code) and 'Q' not in str(code):
            stress_ids.append(i)

pvals = build_linreg_with_age(ecg_table, stress_ids, metrics_dict_age_stress, metrics_dict_ph_age_stress,
                              metrics_dict_delta_stress)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_stress)
metrics_dict_age_stress['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_stress)
metrics_dict_age_stress['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_stress, result_path, 'linreg_age_stress')
plot_linreg(ecg_table, stress_ids, metrics_dict_age_stress, 'age', 'stress', plot_path)
metrics_dict_age_linreg['stress'] = metrics_dict_age_stress['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_stress)
metrics_dict_ph_age_stress['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_stress)
metrics_dict_ph_age_stress['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_stress, result_path, 'linreg_ph_age_stress')
plot_linreg(ecg_table, stress_ids, metrics_dict_ph_age_stress, 'ph_age', 'stress', plot_path)
metrics_dict_ph_age_linreg['stress'] = metrics_dict_ph_age_stress['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_stress)
metrics_dict_delta_stress['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_stress)
metrics_dict_delta_stress['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_stress, result_path, 'linreg_delta_age_stress')
plot_linreg(ecg_table, stress_ids, metrics_dict_delta_stress, 'delta_age', 'stress', plot_path)
metrics_dict_delta_age_linreg['stress'] = metrics_dict_delta_stress['R2']

# Correlation for control subjects with age and delta age
metrics_dict_age_control = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                            'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_control = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                               'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_control = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                              'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

control_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('I'):
        control_ids.append(i)

pvals = build_linreg_with_age(ecg_table, control_ids, metrics_dict_age_control, metrics_dict_ph_age_control,
                              metrics_dict_delta_control)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_control)
metrics_dict_age_control['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_control)
metrics_dict_age_control['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_control, result_path, 'linreg_age_control')
plot_linreg(ecg_table, control_ids, metrics_dict_age_control, 'age', 'control', plot_path)
metrics_dict_age_linreg['control'] = metrics_dict_age_control['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_control)
metrics_dict_ph_age_control['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_control)
metrics_dict_ph_age_control['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_control, result_path, 'linreg_ph_age_control')
plot_linreg(ecg_table, control_ids, metrics_dict_ph_age_control, 'ph_age', 'control', plot_path)
metrics_dict_ph_age_linreg['control'] = metrics_dict_ph_age_control['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_control)
metrics_dict_delta_control['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_control)
metrics_dict_delta_control['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_control, result_path, 'linreg_delta_age_control')
plot_linreg(ecg_table, control_ids, metrics_dict_delta_control, 'delta_age', 'control', plot_path)
metrics_dict_delta_age_linreg['control'] = metrics_dict_delta_control['R2']

# Correlation for anemia subjects with age and delta age
metrics_dict_age_anemia = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                           'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_anemia = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                              'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_anemia = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                             'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

anemia_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('A'):
        anemia_ids.append(i)

pvals = build_linreg_with_age(ecg_table, anemia_ids, metrics_dict_age_anemia, metrics_dict_ph_age_anemia,
                              metrics_dict_delta_anemia)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_anemia)
metrics_dict_age_anemia['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_anemia)
metrics_dict_age_anemia['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_anemia, result_path, 'linreg_age_anemia')
plot_linreg(ecg_table, anemia_ids, metrics_dict_age_anemia, 'age', 'anemia', plot_path)
metrics_dict_age_linreg['anemia'] = metrics_dict_age_anemia['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_anemia)
metrics_dict_ph_age_anemia['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_anemia)
metrics_dict_ph_age_anemia['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_anemia, result_path, 'linreg_ph_age_anemia')
plot_linreg(ecg_table, anemia_ids, metrics_dict_ph_age_anemia, 'ph_age', 'anemia', plot_path)
metrics_dict_ph_age_linreg['anemia'] = metrics_dict_ph_age_anemia['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_anemia)
metrics_dict_delta_anemia['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_anemia)
metrics_dict_delta_anemia['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_anemia, result_path, 'linreg_delta_age_anemia')
plot_linreg(ecg_table, anemia_ids, metrics_dict_delta_anemia, 'delta_age', 'anemia', plot_path)
metrics_dict_delta_age_linreg['anemia'] = metrics_dict_delta_anemia['R2']

# Correlation for hemodialysis subjects with age and delta age
metrics_dict_age_dialysis = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                             'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_dialysis = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                                'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_dialysis = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                               'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

dialysis_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('H'):
        dialysis_ids.append(i)

pvals = build_linreg_with_age(ecg_table, dialysis_ids, metrics_dict_age_dialysis, metrics_dict_ph_age_dialysis,
                              metrics_dict_delta_dialysis)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_dialysis)
metrics_dict_age_dialysis['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_dialysis)
metrics_dict_age_dialysis['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_dialysis, result_path, 'linreg_age_dialysis')
plot_linreg(ecg_table, dialysis_ids, metrics_dict_age_dialysis, 'age', 'dialysis', plot_path)
metrics_dict_age_linreg['dialysis'] = metrics_dict_age_dialysis['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_dialysis)
metrics_dict_ph_age_dialysis['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_dialysis)
metrics_dict_ph_age_dialysis['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_dialysis, result_path, 'linreg_ph_age_dialysis')
plot_linreg(ecg_table, dialysis_ids, metrics_dict_ph_age_dialysis, 'ph_age', 'dialysis', plot_path)
metrics_dict_ph_age_linreg['dialysis'] = metrics_dict_ph_age_dialysis['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_dialysis)
metrics_dict_delta_dialysis['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_dialysis)
metrics_dict_delta_dialysis['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_dialysis, result_path, 'linreg_delta_age_dialysis')
plot_linreg(ecg_table, dialysis_ids, metrics_dict_delta_dialysis, 'delta_age', 'dialysis', plot_path)
metrics_dict_delta_age_linreg['dialysis'] = metrics_dict_delta_dialysis['R2']

# Correlation for healthy (stress and control) subjects with age and delta age
metrics_dict_age_healthy = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                            'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_ph_age_healthy = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                               'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}
metrics_dict_delta_healthy = {'param': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_std': [],
                              'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

healthy_ids = []
for i in range(0, len(code_blood_table)):
    code = code_blood_table[i]
    if str(code).startswith('S'):
        if 'L' not in str(code) and 'Q' not in str(code):
            healthy_ids.append(i)
    elif str(code).startswith('I'):
        healthy_ids.append(i)

pvals = build_linreg_with_age(ecg_table, healthy_ids, metrics_dict_age_healthy, metrics_dict_ph_age_healthy,
                              metrics_dict_delta_healthy)

pval_age_corrected_bh = multiple_test_correction(pvals['age'], 'fdr_bh', metrics_dict_age_healthy)
metrics_dict_age_healthy['linreg_pval_corr_bh'] = pval_age_corrected_bh
pval_age_corrected_bonf = multiple_test_correction(pvals['age'], 'bonferroni', metrics_dict_age_healthy)
metrics_dict_age_healthy['linreg_pval_corr_bonf'] = pval_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_age_healthy, result_path, 'linreg_age_healthy')
plot_linreg(ecg_table, healthy_ids, metrics_dict_age_healthy, 'age', 'healthy', plot_path)
metrics_dict_age_linreg['healthy'] = metrics_dict_age_healthy['R2']

pval_ph_age_corrected_bh = multiple_test_correction(pvals['ph_age'], 'fdr_bh', metrics_dict_ph_age_healthy)
metrics_dict_ph_age_healthy['linreg_pval_corr_bh'] = pval_ph_age_corrected_bh
pval_ph_age_corrected_bonf = multiple_test_correction(pvals['ph_age'], 'bonferroni', metrics_dict_ph_age_healthy)
metrics_dict_ph_age_healthy['linreg_pval_corr_bonf'] = pval_ph_age_corrected_bonf

save_dict_to_xlsx(metrics_dict_ph_age_healthy, result_path, 'linreg_ph_age_healthy')
plot_linreg(ecg_table, healthy_ids, metrics_dict_ph_age_healthy, 'ph_age', 'healthy', plot_path)
metrics_dict_ph_age_linreg['healthy'] = metrics_dict_ph_age_healthy['R2']

pval_delta_corrected_bh = multiple_test_correction(pvals['delta_age'], 'fdr_bh', metrics_dict_delta_healthy)
metrics_dict_delta_healthy['linreg_pval_corr_bh'] = pval_delta_corrected_bh
pval_delta_corrected_bonf = multiple_test_correction(pvals['delta_age'], 'bonferroni', metrics_dict_delta_healthy)
metrics_dict_delta_healthy['linreg_pval_corr_bonf'] = pval_delta_corrected_bonf

save_dict_to_xlsx(metrics_dict_delta_healthy, result_path, 'linreg_delta_age_healthy')
plot_linreg(ecg_table, healthy_ids, metrics_dict_delta_healthy, 'delta_age', 'healthy', plot_path)
metrics_dict_delta_age_linreg['healthy'] = metrics_dict_delta_healthy['R2']

save_dict_to_xlsx(metrics_dict_age_linreg, result_path, 'linreg_age_R2')
save_dict_to_xlsx(metrics_dict_ph_age_linreg, result_path, 'linreg_ph_age_R2')
save_dict_to_xlsx(metrics_dict_delta_age_linreg, result_path, 'linreg_delta_age_R2')
