import os
import math
import pandas as pd
from path import get_path
import statsmodels.api as sm
import numpy as np
from plot import linreg

path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ecg_table_pa = ecg_table[pd.notnull(ecg_table['phenotypic_age'])]
ages = list(ecg_table['age'])
delta_ages = list(ecg_table_pa['delta_age'])
code_blood_table = list(ecg_table['code_blood_table'])
code_blood_table_pa = list(ecg_table_pa['code_blood_table'])
parameters_names = list(ecg_table_pa.columns)[11:]

result_table_path = path + '/linreg/table/'
if not os.path.exists(result_table_path):
    os.makedirs(result_table_path)

result_figure_path = path + '/linreg/plot/'
if not os.path.exists(result_figure_path):
    os.makedirs(result_figure_path)

# Linreg for all subjects

metrics_dict_age = {'param': [], 'R2': [], 'R2_adj': [], 'f_stat': [], 'prob(f_stat)': [], 'log_likelihood': [],
                    'AIC': [], 'BIC': [], 'cond_no': [], 'intercept': [], 'slope': [],
                    'intercept_std': [], 'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

metrics_dict_delta = {'param': [], 'R2': [], 'R2_adj': [], 'f_stat': [], 'prob(f_stat)': [], 'log_likelihood': [],
                      'AIC': [], 'BIC': [], 'cond_no': [], 'intercept': [], 'slope': [],
                      'intercept_std': [], 'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

for param_id in range(0, len(parameters_names)):
    param_name = parameters_names[param_id]
    param_values = list(ecg_table[parameters_names[param_id]])
    param_values_pa = list(ecg_table_pa[parameters_names[param_id]])
    is_age_experiment_not_ok = len(set(param_values)) == 1 \
                               or np.count_nonzero(param_values) < 0.5 * len(param_values)

    is_delta_experiment_not_ok = len(set(param_values_pa)) == 1 \
                                 or np.count_nonzero(param_values_pa) < 0.5 * len(param_values_pa)

    if is_age_experiment_not_ok:

        metrics_dict_age['param'].append(param_name)
        metrics_dict_age['R2'].append('nan')
        metrics_dict_age['R2_adj'].append('nan')
        metrics_dict_age['f_stat'].append('nan')
        metrics_dict_age['prob(f_stat)'].append('nan')
        metrics_dict_age['log_likelihood'].append('nan')
        metrics_dict_age['AIC'].append('nan')
        metrics_dict_age['BIC'].append('nan')
        metrics_dict_age['cond_no'].append('nan')
        metrics_dict_age['intercept'].append('nan')
        metrics_dict_age['slope'].append('nan')
        metrics_dict_age['intercept_std'].append('nan')
        metrics_dict_age['slope_std'].append('nan')
        metrics_dict_age['intercept_p_value'].append('nan')
        metrics_dict_age['slope_p_value'].append('nan')

        if is_delta_experiment_not_ok:

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['R2'].append('nan')
            metrics_dict_delta['R2_adj'].append('nan')
            metrics_dict_delta['f_stat'].append('nan')
            metrics_dict_delta['prob(f_stat)'].append('nan')
            metrics_dict_delta['log_likelihood'].append('nan')
            metrics_dict_delta['AIC'].append('nan')
            metrics_dict_delta['BIC'].append('nan')
            metrics_dict_delta['cond_no'].append('nan')
            metrics_dict_delta['intercept'].append('nan')
            metrics_dict_delta['slope'].append('nan')
            metrics_dict_delta['intercept_std'].append('nan')
            metrics_dict_delta['slope_std'].append('nan')
            metrics_dict_delta['intercept_p_value'].append('nan')
            metrics_dict_delta['slope_p_value'].append('nan')

        else:  # delta experiment is ok
            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(delta_ages[i])
            x_delta = sm.add_constant(curr_delta)
            results_delta = sm.OLS(curr_param_pa, x_delta).fit()

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['R2'].append(results_delta.rsquared)
            metrics_dict_delta['R2_adj'].append(results_delta.rsquared_adj)
            metrics_dict_delta['f_stat'].append(results_delta.fvalue)
            metrics_dict_delta['prob(f_stat)'].append(results_delta.f_pvalue)
            metrics_dict_delta['log_likelihood'].append(results_delta.llf)
            metrics_dict_delta['AIC'].append(results_delta.aic)
            metrics_dict_delta['BIC'].append(results_delta.bic)
            metrics_dict_delta['cond_no'].append(results_delta.condition_number)
            metrics_dict_delta['intercept'].append(results_delta.params[0])
            metrics_dict_delta['slope'].append(results_delta.params[1])
            metrics_dict_delta['intercept_std'].append(results_delta.bse[0])
            metrics_dict_delta['slope_std'].append(results_delta.bse[1])
            metrics_dict_delta['intercept_p_value'].append(results_delta.pvalues[0])
            metrics_dict_delta['slope_p_value'].append(results_delta.pvalues[1])

            if results_delta.rsquared > 0.15:
                linreg([curr_delta, curr_param_pa], [results_delta.params[1], results_delta.params[0]], param_name,
                       results_delta.rsquared, 'Difference between biologic and phenotypic age', 'all_delta',
                       result_figure_path)

    else:  # age experiment is ok

        curr_param = []
        curr_age = []
        for i in range(0, len(param_values)):
            if not math.isnan(param_values[i]):
                curr_param.append(param_values[i])
                curr_age.append(ages[i])
        x_age = sm.add_constant(curr_age)
        results_age = sm.OLS(curr_param, x_age).fit()

        metrics_dict_age['param'].append(param_name)
        metrics_dict_age['R2'].append(results_age.rsquared)
        metrics_dict_age['R2_adj'].append(results_age.rsquared_adj)
        metrics_dict_age['f_stat'].append(results_age.fvalue)
        metrics_dict_age['prob(f_stat)'].append(results_age.f_pvalue)
        metrics_dict_age['log_likelihood'].append(results_age.llf)
        metrics_dict_age['AIC'].append(results_age.aic)
        metrics_dict_age['BIC'].append(results_age.bic)
        metrics_dict_age['cond_no'].append(results_age.condition_number)
        metrics_dict_age['intercept'].append(results_age.params[0])
        metrics_dict_age['slope'].append(results_age.params[1])
        metrics_dict_age['intercept_std'].append(results_age.bse[0])
        metrics_dict_age['slope_std'].append(results_age.bse[1])
        metrics_dict_age['intercept_p_value'].append(results_age.pvalues[0])
        metrics_dict_age['slope_p_value'].append(results_age.pvalues[1])

        if results_age.rsquared > 0.15:
            linreg([curr_age, curr_param], [results_age.params[1], results_age.params[0]], param_name,
                   results_age.rsquared, 'Age', 'all_age', result_figure_path)

        if is_delta_experiment_not_ok:

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['R2'].append('nan')
            metrics_dict_delta['R2_adj'].append('nan')
            metrics_dict_delta['f_stat'].append('nan')
            metrics_dict_delta['prob(f_stat)'].append('nan')
            metrics_dict_delta['log_likelihood'].append('nan')
            metrics_dict_delta['AIC'].append('nan')
            metrics_dict_delta['BIC'].append('nan')
            metrics_dict_delta['cond_no'].append('nan')
            metrics_dict_delta['intercept'].append('nan')
            metrics_dict_delta['slope'].append('nan')
            metrics_dict_delta['intercept_std'].append('nan')
            metrics_dict_delta['slope_std'].append('nan')
            metrics_dict_delta['intercept_p_value'].append('nan')
            metrics_dict_delta['slope_p_value'].append('nan')

        else:  # delta experiment is ok
            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(delta_ages[i])
            x_delta = sm.add_constant(curr_delta)
            results_delta = sm.OLS(curr_param_pa, x_delta).fit()

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['R2'].append(results_delta.rsquared)
            metrics_dict_delta['R2_adj'].append(results_delta.rsquared_adj)
            metrics_dict_delta['f_stat'].append(results_delta.fvalue)
            metrics_dict_delta['prob(f_stat)'].append(results_delta.f_pvalue)
            metrics_dict_delta['log_likelihood'].append(results_delta.llf)
            metrics_dict_delta['AIC'].append(results_delta.aic)
            metrics_dict_delta['BIC'].append(results_delta.bic)
            metrics_dict_delta['cond_no'].append(results_delta.condition_number)
            metrics_dict_delta['intercept'].append(results_delta.params[0])
            metrics_dict_delta['slope'].append(results_delta.params[1])
            metrics_dict_delta['intercept_std'].append(results_delta.bse[0])
            metrics_dict_delta['slope_std'].append(results_delta.bse[1])
            metrics_dict_delta['intercept_p_value'].append(results_delta.pvalues[0])
            metrics_dict_delta['slope_p_value'].append(results_delta.pvalues[1])

            if results_delta.rsquared > 0.15:
                linreg([curr_delta, curr_param_pa], [results_delta.params[1], results_delta.params[0]], param_name,
                       results_delta.rsquared, 'Difference between biologic and phenotypic age', 'all_delta',
                       result_figure_path)

result_df_age = pd.DataFrame.from_dict(metrics_dict_age)
writer = pd.ExcelWriter(result_table_path + 'linreg_age.xlsx', engine='xlsxwriter')
result_df_age.to_excel(writer, index=False)
writer.save()

result_df_delta = pd.DataFrame.from_dict(metrics_dict_delta)
writer = pd.ExcelWriter(result_table_path + 'linreg_delta.xlsx', engine='xlsxwriter')
result_df_delta.to_excel(writer, index=False)
writer.save()

metrics_dict_age_healthy = {'param': [], 'R2': [], 'R2_adj': [], 'f_stat': [], 'prob(f_stat)': [], 'log_likelihood': [],
                            'AIC': [], 'BIC': [], 'cond_no': [], 'intercept': [], 'slope': [],
                            'intercept_std': [], 'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

metrics_dict_delta_healthy = {'param': [], 'R2': [], 'R2_adj': [], 'f_stat': [], 'prob(f_stat)': [],
                              'log_likelihood': [], 'AIC': [], 'BIC': [], 'cond_no': [], 'intercept': [], 'slope': [],
                              'intercept_std': [], 'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

# Linreg for healthy subjects

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
            if list(ecg_table[parameters_names[param_id]]).index(curr_param_value) in healthy_ids['age']:
                param_values.append(curr_param_value)
                healthy_ages.append(ages[i])

    param_values_pa = []
    healthy_delta_ages = []
    for i in range(0, len(list(ecg_table_pa[parameters_names[param_id]]))):
        curr_param_value = list(ecg_table_pa[parameters_names[param_id]])[i]
        if not math.isnan(curr_param_value):
            if list(ecg_table_pa[parameters_names[param_id]]).index(curr_param_value) in healthy_ids['delta']:
                param_values_pa.append(curr_param_value)
                healthy_delta_ages.append(delta_ages[i])

    is_age_experiment_not_ok = len(set(param_values)) == 1 \
                               or np.count_nonzero(param_values) < 0.5 * len(param_values)

    is_delta_experiment_not_ok = len(set(param_values_pa)) == 1 \
                                 or np.count_nonzero(param_values_pa) < 0.5 * len(param_values_pa)

    if is_age_experiment_not_ok:

        metrics_dict_age_healthy['param'].append(param_name)
        metrics_dict_age_healthy['R2'].append('nan')
        metrics_dict_age_healthy['R2_adj'].append('nan')
        metrics_dict_age_healthy['f_stat'].append('nan')
        metrics_dict_age_healthy['prob(f_stat)'].append('nan')
        metrics_dict_age_healthy['log_likelihood'].append('nan')
        metrics_dict_age_healthy['AIC'].append('nan')
        metrics_dict_age_healthy['BIC'].append('nan')
        metrics_dict_age_healthy['cond_no'].append('nan')
        metrics_dict_age_healthy['intercept'].append('nan')
        metrics_dict_age_healthy['slope'].append('nan')
        metrics_dict_age_healthy['intercept_std'].append('nan')
        metrics_dict_age_healthy['slope_std'].append('nan')
        metrics_dict_age_healthy['intercept_p_value'].append('nan')
        metrics_dict_age_healthy['slope_p_value'].append('nan')

        if is_delta_experiment_not_ok:

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['R2'].append('nan')
            metrics_dict_delta_healthy['R2_adj'].append('nan')
            metrics_dict_delta_healthy['f_stat'].append('nan')
            metrics_dict_delta_healthy['prob(f_stat)'].append('nan')
            metrics_dict_delta_healthy['log_likelihood'].append('nan')
            metrics_dict_delta_healthy['AIC'].append('nan')
            metrics_dict_delta_healthy['BIC'].append('nan')
            metrics_dict_delta_healthy['cond_no'].append('nan')
            metrics_dict_delta_healthy['intercept'].append('nan')
            metrics_dict_delta_healthy['slope'].append('nan')
            metrics_dict_delta_healthy['intercept_std'].append('nan')
            metrics_dict_delta_healthy['slope_std'].append('nan')
            metrics_dict_delta_healthy['intercept_p_value'].append('nan')
            metrics_dict_delta_healthy['slope_p_value'].append('nan')

        else:  # delta experiment is ok
            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(healthy_delta_ages[i])
            x_delta = sm.add_constant(curr_delta)
            results_delta = sm.OLS(curr_param_pa, x_delta).fit()

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['R2'].append(results_delta.rsquared)
            metrics_dict_delta_healthy['R2_adj'].append(results_delta.rsquared_adj)
            metrics_dict_delta_healthy['f_stat'].append(results_delta.fvalue)
            metrics_dict_delta_healthy['prob(f_stat)'].append(results_delta.f_pvalue)
            metrics_dict_delta_healthy['log_likelihood'].append(results_delta.llf)
            metrics_dict_delta_healthy['AIC'].append(results_delta.aic)
            metrics_dict_delta_healthy['BIC'].append(results_delta.bic)
            metrics_dict_delta_healthy['cond_no'].append(results_delta.condition_number)
            metrics_dict_delta_healthy['intercept'].append(results_delta.params[0])
            metrics_dict_delta_healthy['slope'].append(results_delta.params[1])
            metrics_dict_delta_healthy['intercept_std'].append(results_delta.bse[0])
            metrics_dict_delta_healthy['slope_std'].append(results_delta.bse[1])
            metrics_dict_delta_healthy['intercept_p_value'].append(results_delta.pvalues[0])
            metrics_dict_delta_healthy['slope_p_value'].append(results_delta.pvalues[1])

            if results_delta.rsquared > 0.15:
                linreg([curr_delta, curr_param_pa], [results_delta.params[1], results_delta.params[0]], param_name,
                       results_delta.rsquared, 'Difference between chronological and phenotypic age', 'healthy_delta',
                       result_figure_path)

    else:  # age experiment is ok

        curr_param = []
        curr_age = []
        for i in range(0, len(param_values)):
            if not math.isnan(param_values[i]):
                curr_param.append(param_values[i])
                curr_age.append(healthy_ages[i])
        x_age = sm.add_constant(curr_age)
        results_age = sm.OLS(curr_param, x_age).fit()

        metrics_dict_age_healthy['param'].append(param_name)
        metrics_dict_age_healthy['R2'].append(results_age.rsquared)
        metrics_dict_age_healthy['R2_adj'].append(results_age.rsquared_adj)
        metrics_dict_age_healthy['f_stat'].append(results_age.fvalue)
        metrics_dict_age_healthy['prob(f_stat)'].append(results_age.f_pvalue)
        metrics_dict_age_healthy['log_likelihood'].append(results_age.llf)
        metrics_dict_age_healthy['AIC'].append(results_age.aic)
        metrics_dict_age_healthy['BIC'].append(results_age.bic)
        metrics_dict_age_healthy['cond_no'].append(results_age.condition_number)
        metrics_dict_age_healthy['intercept'].append(results_age.params[0])
        metrics_dict_age_healthy['slope'].append(results_age.params[1])
        metrics_dict_age_healthy['intercept_std'].append(results_age.bse[0])
        metrics_dict_age_healthy['slope_std'].append(results_age.bse[1])
        metrics_dict_age_healthy['intercept_p_value'].append(results_age.pvalues[0])
        metrics_dict_age_healthy['slope_p_value'].append(results_age.pvalues[1])

        if results_age.rsquared > 0.15:
            linreg([curr_age, curr_param], [results_age.params[1], results_age.params[0]], param_name,
                   results_age.rsquared, 'Age', 'healthy_age', result_figure_path)

        if is_delta_experiment_not_ok:

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['R2'].append('nan')
            metrics_dict_delta_healthy['R2_adj'].append('nan')
            metrics_dict_delta_healthy['f_stat'].append('nan')
            metrics_dict_delta_healthy['prob(f_stat)'].append('nan')
            metrics_dict_delta_healthy['log_likelihood'].append('nan')
            metrics_dict_delta_healthy['AIC'].append('nan')
            metrics_dict_delta_healthy['BIC'].append('nan')
            metrics_dict_delta_healthy['cond_no'].append('nan')
            metrics_dict_delta_healthy['intercept'].append('nan')
            metrics_dict_delta_healthy['slope'].append('nan')
            metrics_dict_delta_healthy['intercept_std'].append('nan')
            metrics_dict_delta_healthy['slope_std'].append('nan')
            metrics_dict_delta_healthy['intercept_p_value'].append('nan')
            metrics_dict_delta_healthy['slope_p_value'].append('nan')

        else:  # delta experiment is ok
            curr_param_pa = []
            curr_delta = []
            for i in range(0, len(param_values_pa)):
                if not math.isnan(param_values_pa[i]):
                    curr_param_pa.append(param_values_pa[i])
                    curr_delta.append(healthy_delta_ages[i])
            x_delta = sm.add_constant(curr_delta)
            results_delta = sm.OLS(curr_param_pa, x_delta).fit()

            metrics_dict_delta_healthy['param'].append(param_name)
            metrics_dict_delta_healthy['R2'].append(results_delta.rsquared)
            metrics_dict_delta_healthy['R2_adj'].append(results_delta.rsquared_adj)
            metrics_dict_delta_healthy['f_stat'].append(results_delta.fvalue)
            metrics_dict_delta_healthy['prob(f_stat)'].append(results_delta.f_pvalue)
            metrics_dict_delta_healthy['log_likelihood'].append(results_delta.llf)
            metrics_dict_delta_healthy['AIC'].append(results_delta.aic)
            metrics_dict_delta_healthy['BIC'].append(results_delta.bic)
            metrics_dict_delta_healthy['cond_no'].append(results_delta.condition_number)
            metrics_dict_delta_healthy['intercept'].append(results_delta.params[0])
            metrics_dict_delta_healthy['slope'].append(results_delta.params[1])
            metrics_dict_delta_healthy['intercept_std'].append(results_delta.bse[0])
            metrics_dict_delta_healthy['slope_std'].append(results_delta.bse[1])
            metrics_dict_delta_healthy['intercept_p_value'].append(results_delta.pvalues[0])
            metrics_dict_delta_healthy['slope_p_value'].append(results_delta.pvalues[1])

            if results_delta.rsquared > 0.15:
                linreg([curr_delta, curr_param_pa], [results_delta.params[1], results_delta.params[0]], param_name,
                       results_delta.rsquared, 'Difference between chronological and phenotypic age', 'healthy_delta',
                       result_figure_path)

result_df_age = pd.DataFrame.from_dict(metrics_dict_age_healthy)
writer = pd.ExcelWriter(result_table_path + 'linreg_healthy_age.xlsx', engine='xlsxwriter')
result_df_age.to_excel(writer, index=False)
writer.save()

result_df_delta = pd.DataFrame.from_dict(metrics_dict_delta_healthy)
writer = pd.ExcelWriter(result_table_path + 'linreg_healthy_delta.xlsx', engine='xlsxwriter')
result_df_delta.to_excel(writer, index=False)
writer.save()
