import plotly
import plotly.graph_objects as go
import colorlover as cl


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


def boxplot(data, names, param, pval, path):
    traces = []
    i = 0
    for key in data:
        name = names[i]

        color = cl.scales['8']['qual']['Set1'][i]
        coordinates = color[4:-1].split(',')
        marker_color = 'rgba(' + ','.join(coordinates) + ',' + str(0.5) + ')'
        line_color = 'rgba(' + ','.join(coordinates) + ',' + str(1.0) + ')'

        trace = go.Box(
            y=data[key],
            name=name,
            boxpoints='outliers',
            marker_color=marker_color,
            line_color=line_color
        )

        traces.append(trace)
        i += 1

    layout = go.Layout(
        autosize=True,
        showlegend=False,
        xaxis=get_axis(''),
        yaxis=get_axis(''),
        title={
            'text': param + ' p-value: ' + str(pval),
            'x': 0.5,
            'y': 0.9},
        titlefont=dict(
            family='Arial',
            color='black',
            size=24),
    )

    fig = go.Figure(data=traces, layout=layout)

    plotly.offline.plot(fig, filename=path + 'boxplot_' + '_'.join(list(data.keys())) + '_' + param + '.html',
                        auto_open=False, show_link=True)
    plotly.io.write_image(fig, path + 'boxplot_' + '_'.join(list(data.keys())) + '_' + param + '.png')
    plotly.io.write_image(fig, path + 'boxplot_' + '_'.join(list(data.keys())) + '_' + param + '.pdf')


def linreg(data, line, param, r2, age_type, suffix, path):
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
        xaxis=get_axis(age_type),
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

    plotly.offline.plot(fig, filename=path + 'linreg_' + suffix + '_' + param + '.html', auto_open=False,
                        show_link=True)
    plotly.io.write_image(fig, path + 'linreg_' + suffix + '_' + param + '.png')
    plotly.io.write_image(fig, path + 'linreg_' + suffix + '_' + param + '.pdf')
