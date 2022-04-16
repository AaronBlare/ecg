import numpy as np
import pandas as pd
from pathlib import Path


path = 'E:/YandexDisk/ECG/files/'
data_path = 'E:/YandexDisk/ECG/'
data_file = 'ecg_snp_data_info.xlsx'

df = pd.read_excel(data_path + data_file)
df = df.rename(columns={'code_blood_table': 'index'})

features_names = list(df.columns.values)[1:-2]
features_df = pd.DataFrame.from_dict({'features': features_names})

df.to_excel(f"{path}/ecg_df.xlsx", header=True, index=False)
features_df.to_excel(f"{path}/features_df.xlsx", header=True, index=False)
