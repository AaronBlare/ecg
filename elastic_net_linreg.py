import pandas as pd
import plotly
import plotly.graph_objects as go
import os
from path import get_path
from plot_scatter import get_axis
import statsmodels.api as sm


y_name = 'phenotypic_age'  # age or phenotypic_age
part = 'wo_subj'

target_part = 'Control'
data_type = 'ECG'

path = get_path()

df_merged = pd.read_excel(f'{path}/table/ecg_data_{part}.xlsx', engine='openpyxl')

save_path = f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/plot'
if not os.path.exists(save_path):
    os.makedirs(save_path)

features = pd.read_excel(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/clock.xlsx', engine='openpyxl')
target_features = list(features['feature'])[1:]

metrics_dict = {'feature': [], 'R2': [], 'intercept': [], 'slope': [], 'intercept_p_value': [], 'slope_p_value': []}

for feature in target_features:
    X_C = df_merged[y_name].to_numpy()
    y_C = df_merged[feature].to_numpy()

    x = sm.add_constant(X_C)
    results = sm.OLS(y_C, x).fit()

    metrics_dict['feature'].append(feature)
    metrics_dict['R2'].append(results.rsquared)
    metrics_dict['intercept'].append(results.params[0])
    metrics_dict['slope'].append(results.params[1])
    metrics_dict['intercept_p_value'].append(results.pvalues[0])
    metrics_dict['slope_p_value'].append(results.pvalues[1])

    traces = []
    trace = go.Scatter(
        x=X_C,
        y=y_C,
        mode='markers',
        marker=dict(
            size=8,
            line=dict(
                width=0.5
            ),
            opacity=0.8
        )
    )
    traces.append(trace)

    slope = results.params[1]
    intercept = results.params[0]

    x_line = [min(X_C), max(X_C)]
    y_line = [slope * x_line[0] + intercept, slope * x_line[1] + intercept]
    linreg_line = go.Scatter(x=x_line, y=y_line, mode='lines')
    traces.append(linreg_line)

    layout = go.Layout(
        autosize=True,
        showlegend=False,
        xaxis=get_axis(y_name),
        yaxis=get_axis(feature)
    )

    fig = go.Figure(data=traces, layout=layout)

    plotly.io.write_image(fig, f'{save_path}/{feature}.png')
    plotly.io.write_image(fig, f'{save_path}/{feature}.pdf')


result_df = pd.DataFrame.from_dict(metrics_dict)
writer = pd.ExcelWriter(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/linreg.xlsx', engine='xlsxwriter')
result_df.to_excel(writer, index=False)
writer.save()
