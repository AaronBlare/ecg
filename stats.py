import os
import plotly
import pandas as pd
from path import get_path
import plotly.graph_objects as go

path = get_path()
result_path = path + '/stats/'
if not os.path.exists(result_path):
    os.makedirs(result_path)

ecg_table = pd.read_excel(path + '/ecg_data_info.xlsx')
ecg_table_pa = ecg_table[pd.notnull(ecg_table['phenotypic_age'])]
ages = list(ecg_table['age'])
sex = list(ecg_table['sex'])
delta_ages = list(ecg_table_pa['delta_age'])
sex_pa = list(ecg_table_pa['sex'])

males_ages = []
females_ages = []
for i in range(0, len(ages)):
    if sex[i] == 'Male':
        males_ages.append(ages[i])
    else:
        females_ages.append(ages[i])

fig = go.Figure()
fig.add_trace(go.Histogram(x=females_ages,
                           marker_color='red',
                           opacity=0.65,
                           name='Females',
                           xbins=dict(size=2)))
fig.add_trace(go.Histogram(x=males_ages,
                           marker_color='blue',
                           opacity=0.65,
                           name='Males',
                           xbins=dict(size=2)))
fig.update_layout(autosize=True,
                  showlegend=True,
                  title={
                      'text': 'Age',
                      'x': 0.5,
                      'y': 0.9},
                  titlefont=dict(
                      family='Arial',
                      color='black',
                      size=24),
                  barmode='overlay')
plotly.offline.plot(fig, filename=result_path + 'pdf_age.html', auto_open=False, show_link=True)
plotly.io.write_image(fig, result_path + 'pdf_age.png')
plotly.io.write_image(fig, result_path + 'pdf_age.pdf')

males_delta_ages = []
females_delta_ages = []
for i in range(0, len(delta_ages)):
    if sex_pa[i] == 'Male':
        males_delta_ages.append(delta_ages[i])
    else:
        females_delta_ages.append(delta_ages[i])

fig = go.Figure()
fig.add_trace(go.Histogram(x=females_delta_ages,
                           marker_color='red',
                           opacity=0.65,
                           name='Females',
                           xbins=dict(size=2)))
fig.add_trace(go.Histogram(x=males_delta_ages,
                           marker_color='blue',
                           opacity=0.65,
                           name='Males',
                           xbins=dict(size=2)))
fig.update_layout(autosize=True,
                  showlegend=True,
                  title={
                      'text': 'Difference between chronological and phenotypic age',
                      'x': 0.5,
                      'y': 0.9},
                  titlefont=dict(
                      family='Arial',
                      color='black',
                      size=24),
                  barmode='overlay')
plotly.offline.plot(fig, filename=result_path + 'pdf_delta_age.html', auto_open=False, show_link=True)
plotly.io.write_image(fig, result_path + 'pdf_delta_age.png')
plotly.io.write_image(fig, result_path + 'pdf_delta_age.pdf')
