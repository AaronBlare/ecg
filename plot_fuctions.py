import os
import plotly
import plotly.graph_objects as go


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


def linreg(data, line, param, r2, age_name, age_type, suffix, path):
    traces = []
    trace = go.Scatter(
        x=data[0],
        y=data[1],
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

    x_line = [min(data[0]), max(data[0])]
    y_line = [line[0] * x_line[0] + line[1], line[0] * x_line[1] + line[1]]
    linreg_line = go.Scatter(x=x_line, y=y_line, mode='lines')
    traces.append(linreg_line)

    layout = go.Layout(
        autosize=True,
        showlegend=False,
        xaxis=get_axis(age_name),
        yaxis=get_axis(param),
        title={
            'text': 'R2: ' + str(r2),
            'x': 0.5,
            'y': 0.9},
        titlefont=dict(
            family='Arial',
            color='black',
            size=24),
    )

    fig = go.Figure(data=traces, layout=layout)

    if not os.path.exists(path + suffix):
        os.makedirs(path + suffix)

    plotly.io.write_image(fig, path + suffix + '/linreg_' + age_type + '_' + suffix + '_' + param + '.png')
    plotly.io.write_image(fig, path + suffix + '/linreg_' + age_type + '_' + suffix + '_' + param + '.pdf')
