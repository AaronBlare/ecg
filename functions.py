import math
from scipy.stats import spearmanr, pearsonr
from statsmodels.stats.multitest import multipletests


def subset_curr_ages(ecg_table, ids, param_name):

    ages = list(ecg_table['age'])
    delta_ages = list(ecg_table['delta_age'])

    param_values = []
    subset_ages = []
    subset_delta_ages = []

    for i in range(0, len(list(ecg_table[param_name]))):
        curr_param_value = list(ecg_table[param_name])[i]
        if not math.isnan(curr_param_value):
            if i in ids:
                param_values.append(curr_param_value)
                subset_ages.append(ages[i])
                subset_delta_ages.append(delta_ages[i])

    return subset_ages, subset_delta_ages, param_values


def calculate_correlation_with_age(ecg_table, ids,
                                   metrics_dict_age, metrics_dict_delta):

    parameters_names = list(ecg_table.columns)[12:]

    pvals_age = []
    pvals_delta_age = []

    for param_id in range(0, len(parameters_names)):
        param_name = parameters_names[param_id]
        ages, delta_ages, param_values = subset_curr_ages(ecg_table, ids, param_name)

        if len(set(param_values)) <= 1:
            metrics_dict_age['param'].append(param_name)
            metrics_dict_age['spearman_rho'].append('nan')
            metrics_dict_age['spearman_pval'].append('nan')
            metrics_dict_age['pearson_coef'].append('nan')
            metrics_dict_age['pearson_pval'].append('nan')

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

            spearman_results_delta = spearmanr(delta_ages, param_values)
            pearson_results_delta = pearsonr(delta_ages, param_values)

            metrics_dict_delta['param'].append(param_name)
            metrics_dict_delta['spearman_rho'].append(spearman_results_delta[0])
            metrics_dict_delta['spearman_pval'].append(spearman_results_delta[1])
            metrics_dict_delta['pearson_coef'].append(pearson_results_delta[0])
            metrics_dict_delta['pearson_pval'].append(pearson_results_delta[1])
            pvals_delta_age.append(spearman_results_delta[1])

    return pvals_age, pvals_delta_age


def multiple_test_correction(pvals, method, metrics_dict_age):

    reject_bh, pvals_corr_bh, alphacSidak_bh, alphacBonf_bh = multipletests(pvals, 0.05, method=method)

    pval_age_corrected = []
    original_index_age = 0
    for i in range(0, len(metrics_dict_age['param'])):
        if metrics_dict_age['spearman_pval'][i] == 'nan':
            pval_age_corrected.append('nan')
        else:
            pval_age_corrected.append(pvals_corr_bh[original_index_age])
            original_index_age += 1

    return pval_age_corrected

