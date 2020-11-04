import pandas as pd


def save_dict_to_xlsx(metrics_dict, result_path, name):

    result_df_age = pd.DataFrame.from_dict(metrics_dict)
    writer = pd.ExcelWriter(result_path + name + '.xlsx', engine='xlsxwriter')
    result_df_age.to_excel(writer, index=False)
    writer.save()

