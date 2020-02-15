import os
import math
import pandas as pd
from path import get_path
import statsmodels.api as sm

path = get_path()
ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ecg_table_pa = ecg_table[pd.notnull(ecg_table['phenotypic_age'])]
ages = list(ecg_table_pa['age'])
delta_ages = list(ecg_table_pa['delta_age'])
parameters_names = list(ecg_table_pa.columns)[11:]

metrics_dict_age = {'param': [], 'R2': [], 'R2_adj': [], 'f_stat': [], 'prob(f_stat)': [], 'log_likelihood': [],
                    'AIC': [], 'BIC': [], 'cond_no': [], 'intercept': [], 'slope': [],
                    'intercept_std': [], 'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

metrics_dict_delta = {'param': [], 'R2': [], 'R2_adj': [], 'f_stat': [], 'prob(f_stat)': [], 'log_likelihood': [],
                      'AIC': [], 'BIC': [], 'cond_no': [], 'intercept': [], 'slope': [],
                      'intercept_std': [], 'slope_std': [], 'intercept_p_value': [], 'slope_p_value': []}

for param_id in range(0, len(parameters_names)):
    param_name = parameters_names[param_id]
    param_values = list(ecg_table_pa[parameters_names[param_id]])
    if len(set(param_values)) == 1:
        metrics_dict_age['param'].append(param_name)
        metrics_dict_age['R2'].append(0)
        metrics_dict_age['R2_adj'].append(0)
        metrics_dict_age['f_stat'].append(0)
        metrics_dict_age['prob(f_stat)'].append(0)
        metrics_dict_age['log_likelihood'].append(0)
        metrics_dict_age['AIC'].append(0)
        metrics_dict_age['BIC'].append(0)
        metrics_dict_age['cond_no'].append(0)
        metrics_dict_age['intercept'].append(0)
        metrics_dict_age['slope'].append(0)
        metrics_dict_age['intercept_std'].append(0)
        metrics_dict_age['slope_std'].append(0)
        metrics_dict_age['intercept_p_value'].append(0)
        metrics_dict_age['slope_p_value'].append(0)

        metrics_dict_delta['param'].append(param_name)
        metrics_dict_delta['R2'].append(0)
        metrics_dict_delta['R2_adj'].append(0)
        metrics_dict_delta['f_stat'].append(0)
        metrics_dict_delta['prob(f_stat)'].append(0)
        metrics_dict_delta['log_likelihood'].append(0)
        metrics_dict_delta['AIC'].append(0)
        metrics_dict_delta['BIC'].append(0)
        metrics_dict_delta['cond_no'].append(0)
        metrics_dict_delta['intercept'].append(0)
        metrics_dict_delta['slope'].append(0)
        metrics_dict_delta['intercept_std'].append(0)
        metrics_dict_delta['slope_std'].append(0)
        metrics_dict_delta['intercept_p_value'].append(0)
        metrics_dict_delta['slope_p_value'].append(0)
        continue

    curr_param = []
    curr_age = []
    curr_delta = []
    for i in range(0, len(param_values)):
        if not math.isnan(param_values[i]):
            curr_param.append(param_values[i])
            curr_age.append(ages[i])
            curr_delta.append(delta_ages[i])
    x_age = sm.add_constant(curr_age)
    x_delta = sm.add_constant(curr_delta)
    results_age = sm.OLS(curr_param, x_age).fit()
    results_delta = sm.OLS(curr_param, x_delta).fit()

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

result_path = path + '/linreg/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

result_df_age = pd.DataFrame.from_dict(metrics_dict_age)
writer = pd.ExcelWriter(result_path + 'linreg_age.xlsx', engine='xlsxwriter')
result_df_age.to_excel(writer, index=False)
writer.save()

result_df_delta = pd.DataFrame.from_dict(metrics_dict_delta)
writer = pd.ExcelWriter(result_path + 'linreg_delta.xlsx', engine='xlsxwriter')
result_df_delta.to_excel(writer, index=False)
writer.save()
