import pandas as pd
import plotly
import plotly.graph_objects as go
import os
from path import get_path


def get_axis(title):
    axis = dict(
        title=title,
        showgrid=True,
        showline=True,
        mirror='ticks',
        titlefont=dict(
            family='Arial',
            color='black',
            size=24,
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='Arial',
            color='black',
            size=20
        ),
        exponentformat='e',
        showexponent='all'
    )
    return axis


y_name = 'phenotypic_age'  # age or phenotypic_age
part = 'snp_wo_subj'

target_part = 'Control'
data_type = 'ECG'

path = get_path()

df_merged = pd.read_excel(f'{path}/table/ecg_data_{part}.xlsx', engine='openpyxl')

save_path = f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/plot'
if not os.path.exists(save_path):
    os.makedirs(save_path)

features = pd.read_excel(f'{path}/clock/{data_type}/{target_part}/{y_name}/{part}/clock.xlsx', engine='openpyxl')
target_features = list(features['feature'])[1:]

for feature in target_features:
    X_C = df_merged[y_name].to_numpy()
    y_C = df_merged[feature].to_numpy()

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

    layout = go.Layout(
        autosize=True,
        showlegend=False,
        xaxis=get_axis(y_name),
        yaxis=get_axis(feature)
    )

    fig = go.Figure(data=traces, layout=layout)

    plotly.io.write_image(fig, f'{save_path}/{feature}.png')
    plotly.io.write_image(fig, f'{save_path}/{feature}.pdf')
