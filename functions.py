import math
import statsmodels.api as sm
from scipy.stats import spearmanr, pearsonr, pointbiserialr
from statsmodels.stats.multitest import multipletests


def subset_curr_ages(ecg_table, ids, param_name):

    ages = list(ecg_table['age'])
    ph_ages = list(ecg_table['phenotypic_age'])
    delta_ages = list(ecg_table['delta_age'])

    param_values = []
    subset_ages = []
    subset_ph_ages = []
    subset_delta_ages = []

    for i in range(0, len(list(ecg_table[param_name]))):
        curr_param_value = list(ecg_table[param_name])[i]
        if not math.isnan(curr_param_value):
            if i in ids:
                param_values.append(curr_param_value)
                subset_ages.append(ages[i])
                subset_ph_ages.append(ph_ages[i])
                subset_delta_ages.append(delta_ages[i])

    return subset_ages, subset_ph_ages, subset_delta_ages, param_values


def subset_curr_sexes(ecg_table, ids, param_name):

    sex = list(ecg_table['sex'])
    for i in range(0, len(sex)):
        if sex[i] == 'Female':
            sex[i] = 0
        elif sex[i] == 'Male':
            sex[i] = 1
        else:
            sex[i] = 'nan'

    param_values = []
    subset_sexes = []

    for i in range(0, len(list(ecg_table[param_name]))):
        curr_param_value = list(ecg_table[param_name])[i]
        if not math.isnan(curr_param_value):
            if i in ids:
                param_values.append(curr_param_value)
                subset_sexes.append(sex[i])

    return subset_sexes, param_values


def calculate_correlation_with_age(ecg_table, ids,
                                   metrics_dict_age,
                                   metrics_dict_ph_age,
                                   metrics_dict_delta):

    parameters_names = list(ecg_table.columns)[12:]

    pvals_age = []
    pvals_ph_age = []
    pvals_delta_age = []

    for param_id in range(0, len(parameters_names)):
        param_name = parameters_names[param_id]
        ages, ph_ages, delta_ages, param_values = subset_curr_ages(ecg_table, ids, param_name)

        if len(set(param_values)) <= 1:
            metrics_dict_age['param'].append(param_name)
            metrics_dict_age['spearman_rho'].append('nan')
            metrics_dict_age['spearman_pval'].append('nan')
            metrics_dict_age['pearson_coef'].append('nan')
            metrics_dict_age['pearson_pval'].append('nan')

            metrics_dict_ph_age['param'].append(param_name)
            metrics_dict_ph_age['spearman_rho'].append('nan')
            metrics_dict_ph_age['spearman_pval'].append('nan')
            metrics_dict_ph_age['pearson_coef'].append('nan')
            metrics_dict_ph_age['pearson_pval'].append('nan')

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['spearman_rho'].append('nan')
            metrics_dict_delta['spearman_pval'].append('nan')
            metrics_dict_delta['pearson_coef'].append('nan')
            metrics_dict_delta['pearson_pval'].append('nan')

        else:

            spearman_results_age = spearmanr(ages, param_values)
            pearson_results_age = pearsonr(ages, param_values)

            metrics_dict_age['param'].append(param_name)
            metrics_dict_age['spearman_rho'].append(spearman_results_age[0])
            metrics_dict_age['spearman_pval'].append(spearman_results_age[1])
            metrics_dict_age['pearson_coef'].append(pearson_results_age[0])
            metrics_dict_age['pearson_pval'].append(pearson_results_age[1])
            pvals_age.append(spearman_results_age[1])

            spearman_results_ph_age = spearmanr(ph_ages, param_values)
            pearson_results_ph_age = pearsonr(ph_ages, param_values)

            metrics_dict_ph_age['param'].append(param_name)
            metrics_dict_ph_age['spearman_rho'].append(spearman_results_ph_age[0])
            metrics_dict_ph_age['spearman_pval'].append(spearman_results_ph_age[1])
            metrics_dict_ph_age['pearson_coef'].append(pearson_results_ph_age[0])
            metrics_dict_ph_age['pearson_pval'].append(pearson_results_ph_age[1])
            pvals_ph_age.append(spearman_results_ph_age[1])

            spearman_results_delta = spearmanr(delta_ages, param_values)
            pearson_results_delta = pearsonr(delta_ages, param_values)

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta['pearson_pval'].append(pearson_results_delta[1])
            pvals_delta_age.append(spearman_results_delta[1])

    return pvals_age, pvals_ph_age, pvals_delta_age


def calculate_correlation_with_sex(ecg_table, ids,
                                   metrics_dict_sex):

    parameters_names = list(ecg_table.columns)[12:]

    pvals_sex = []

    for param_id in range(0, len(parameters_names)):
        param_name = parameters_names[param_id]
        sexes, param_values = subset_curr_sexes(ecg_table, ids, param_name)

        if len(set(param_values)) <= 1:
            metrics_dict_sex['param'].append(param_name)
            metrics_dict_sex['point_biserial_coeff'].append('nan')
            metrics_dict_sex['point_biserial_pval'].append('nan')

        else:

            point_biserial_results_sex = pointbiserialr(sexes, param_values)

            metrics_dict_sex['param'].append(param_name)
            metrics_dict_sex['point_biserial_coeff'].append(point_biserial_results_sex[0])
            metrics_dict_sex['point_biserial_pval'].append(point_biserial_results_sex[1])
            pvals_sex.append(point_biserial_results_sex[1])

    return pvals_sex


def multiple_test_correction(pvals, method, metrics_dict):

    reject_bh, pvals_corr_bh, alphacSidak_bh, alphacBonf_bh = multipletests(pvals, 0.05, method=method)
    if 'spearman_pval' in metrics_dict:
        pval = metrics_dict['spearman_pval']
    elif 'slope_p_value' in metrics_dict:
        pval = metrics_dict['slope_p_value']
    elif 'point_biserial_pval' in metrics_dict:
        pval = metrics_dict['point_biserial_pval']

    pval_age_corrected = []
    original_index_age = 0
    for i in range(0, len(metrics_dict['param'])):
        if pval[i] == 'nan':
            pval_age_corrected.append('nan')
        else:
            pval_age_corrected.append(pvals_corr_bh[original_index_age])
            original_index_age += 1

    return pval_age_corrected


def build_linreg_with_age(ecg_table, ids,
                          metrics_dict_age,
                          metrics_dict_ph_age,
                          metrics_dict_delta):

    parameters_names = list(ecg_table.columns)[12:]

    pvals_age = []
    pvals_ph_age = []
    pvals_delta_age = []

    for param_id in range(0, len(parameters_names)):
        param_name = parameters_names[param_id]
        ages, ph_ages, delta_ages, param_values = subset_curr_ages(ecg_table, ids, param_name)

        if len(set(param_values)) <= 1:
            metrics_dict_age['param'].append(param_name)
            metrics_dict_age['R2'].append('nan')
            metrics_dict_age['intercept'].append('nan')
            metrics_dict_age['slope'].append('nan')
            metrics_dict_age['intercept_std'].append('nan')
            metrics_dict_age['slope_std'].append('nan')
            metrics_dict_age['intercept_p_value'].append('nan')
            metrics_dict_age['slope_p_value'].append('nan')

            metrics_dict_ph_age['param'].append(param_name)
            metrics_dict_ph_age['R2'].append('nan')
            metrics_dict_ph_age['intercept'].append('nan')
            metrics_dict_ph_age['slope'].append('nan')
            metrics_dict_ph_age['intercept_std'].append('nan')
            metrics_dict_ph_age['slope_std'].append('nan')
            metrics_dict_ph_age['intercept_p_value'].append('nan')
            metrics_dict_ph_age['slope_p_value'].append('nan')

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['R2'].append('nan')
            metrics_dict_delta['intercept'].append('nan')
            metrics_dict_delta['slope'].append('nan')
            metrics_dict_delta['intercept_std'].append('nan')
            metrics_dict_delta['slope_std'].append('nan')
            metrics_dict_delta['intercept_p_value'].append('nan')
            metrics_dict_delta['slope_p_value'].append('nan')

        else:

            x_age = sm.add_constant(ages)
            results_age = sm.OLS(param_values, x_age).fit()

            metrics_dict_age['param'].append(param_name)
            metrics_dict_age['R2'].append(results_age.rsquared)
            metrics_dict_age['intercept'].append(results_age.params[0])
            metrics_dict_age['slope'].append(results_age.params[1])
            metrics_dict_age['intercept_std'].append(results_age.bse[0])
            metrics_dict_age['slope_std'].append(results_age.bse[1])
            metrics_dict_age['intercept_p_value'].append(results_age.pvalues[0])
            metrics_dict_age['slope_p_value'].append(results_age.pvalues[1])
            pvals_age.append(results_age.pvalues[1])

            x_ph_age = sm.add_constant(ph_ages)
            results_ph_age = sm.OLS(param_values, x_ph_age).fit()

            metrics_dict_ph_age['param'].append(param_name)
            metrics_dict_ph_age['R2'].append(results_ph_age.rsquared)
            metrics_dict_ph_age['intercept'].append(results_ph_age.params[0])
            metrics_dict_ph_age['slope'].append(results_ph_age.params[1])
            metrics_dict_ph_age['intercept_std'].append(results_ph_age.bse[0])
            metrics_dict_ph_age['slope_std'].append(results_ph_age.bse[1])
            metrics_dict_ph_age['intercept_p_value'].append(results_ph_age.pvalues[0])
            metrics_dict_ph_age['slope_p_value'].append(results_ph_age.pvalues[1])
            pvals_ph_age.append(results_ph_age.pvalues[1])

            x_delta_age = sm.add_constant(delta_ages)
            results_delta_age = sm.OLS(param_values, x_delta_age).fit()

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['R2'].append(results_delta_age.rsquared)
            metrics_dict_delta['intercept'].append(results_delta_age.params[0])
            metrics_dict_delta['slope'].append(results_delta_age.params[1])
            metrics_dict_delta['intercept_std'].append(results_delta_age.bse[0])
            metrics_dict_delta['slope_std'].append(results_delta_age.bse[1])
            metrics_dict_delta['intercept_p_value'].append(results_delta_age.pvalues[0])
            metrics_dict_delta['slope_p_value'].append(results_delta_age.pvalues[1])
            pvals_delta_age.append(results_delta_age.pvalues[1])

    return pvals_age, pvals_ph_age, pvals_delta_age
