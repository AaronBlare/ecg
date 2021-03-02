import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import RepeatedKFold, GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import pickle
from pathlib import Path
import os
import copy
from path import get_path


def calc_metrics(model, X, y, comment, params):
    y_pred = model.predict(X)
    score = model.score(X, y)
    rmse = np.sqrt(mean_squared_error(y_pred, y))
    mae = mean_absolute_error(y_pred, y)
    params[f'{comment} R2'] = score
    params[f'{comment} RMSE'] = rmse
    params[f'{comment} MAE'] = mae
    return y_pred


y_name = 'phenotypic_age'  # age or phenotypic_age
part = 'wo_subj'
target_part = 'Control'
data_type = 'ECG'

path = get_path()
df_merged = pd.read_excel(f'{path}/table/ecg_data_{part}.xlsx', engine='openpyxl')

save_path = f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}'
if not os.path.exists(save_path):
    os.makedirs(save_path)

with open(f'{path}/table/features_list_{part}.txt') as f:
    target_features = f.read().splitlines()

X_target = df_merged[list(target_features)].to_numpy()
y_target = df_merged[y_name].to_numpy()

# define model evaluation method
cv = RepeatedKFold(n_splits=3, n_repeats=10, random_state=1)

# define model
model_type = ElasticNet(max_iter=10000, tol=0.001)
# define grid
grid = dict()
grid['alpha'] = np.logspace(-5, 1, 61)
grid['l1_ratio'] = np.linspace(0.0, 1.0, 11)
# grid['l1_ratio'] = [0.5]
# define search
scoring = 'r2'
search = GridSearchCV(estimator=model_type, scoring=scoring, param_grid=grid, cv=cv, verbose=3)
# perform the search
results = search.fit(X_target, y_target)
# summarize

model = search.best_estimator_

score = model.score(X_target, y_target)

params = copy.deepcopy(results.best_params_)

searching_process = pd.DataFrame(search.cv_results_)
searching_process.to_excel(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/searching_process_{scoring}.xlsx',
                           index=False)

model_dict = {'feature': ['Intercept'], 'coef': [model.intercept_]}
num_features = 0
for f_id, f in enumerate(target_features):
    coef = model.coef_[f_id]
    if abs(coef) > 0:
        model_dict['feature'].append(f)
        model_dict['coef'].append(coef)
        num_features += 1
model_df = pd.DataFrame(model_dict)

Path(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/').mkdir(parents=True, exist_ok=True)
model_df.to_excel(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/clock.xlsx', index=False)

with open(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/clock.pkl', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

y_pred_C = calc_metrics(model, X_target, y_target, 'Control', params)
params['num_features'] = num_features
params_df = pd.DataFrame({'Feature': list(params.keys()), 'Value': list(params.values())})
params_df.to_excel(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/params.xlsx', index=False)

print(params_df)
