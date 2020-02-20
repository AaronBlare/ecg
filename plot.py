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
