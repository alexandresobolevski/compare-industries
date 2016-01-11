__author__ = 'Alexandre'

py.sign_in('sobolevski.a', '1gd9i51p36')

import pandas as pd
import plotly.plotly as py
import collections
from plotly import graph_objs as go


def make_text(X):
    print X
    return 'Company: %s\
    <br>Return on Assets: %s %%\
    <br>Profit Margin: %s %%\
    <br>Market Cap: %s $B'\
    % (X['name'], X['roa'], X['prm'], X['mc']/1000000000)


def make_trace(frame, sizes, segments, colors):
    X = frame.to_dict('list')
    sizeref = (sizes.max() / 1e2 ** 2)*4
    return go.Scatter(
        x=X['roa'],
        y=X['prm'],
        name=segments,
        mode='markers',
        marker=go.Marker(
            color=colors,
            size=sizes,
            sizeref=sizeref,
            sizemode='area',
            opacity=0.6,
            line=go.Line(width=0.0)
        )
    )


def get_most_popular(category, stats, how_many):
    counted = collections.Counter(stats[category])
    top_sorted = [(l, k) for k, l in sorted(
        [(j, i) for i, j in counted.items()], reverse=True)]
    industries_sorted = [name for name, _ in top_sorted]
    return industries_sorted[:how_many]


def make_plotly_data(stats, top_sorted):
    data = go.Data()
    counter = 0
    colors_array = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                    '#9467bd']
    for industry, X in stats.groupby('industry'):
        if counter > top_sorted: break
        if industry in top_sorted:
            counter += 1
            # print X
            sizes = X['mc']
            color = colors_array[counter - 1]
            data.append(
                make_trace(X, sizes, industry, color))
    return data


def set_layout(x_title, y_title):
    axis_style = dict(
        zeroline=False,
        gridcolor='#FFFFFF',  # white
        ticks='outside',
        ticklen=8,
        tickwidth=1.5
    )

    layout = go.Layout(
        title=title,
        width=1000,
        height=1000,
        hovermode='closest',
        xaxis=go.XAxis(
            axis_style,
            title=x_title,
            range=[0, 25]
        ),
        yaxis=go.YAxis(
            axis_style,
            title=y_title,
            range=[-10, 60]
        )
    )
    return layout

def hover_over_text(fig, stats, top_sorted):
    counter = 0
    for industry, X in stats.groupby('industry'):
        if industry in top_sorted:
            text = X.apply(make_text, axis=1).tolist()
            fig['data'][counter].update(text=text)
            counter += 1
    return fig


def add_data_source_note(fig):
    fig['layout'].update(annotations=go.Annotations([
        go.Annotation(
            text='Data source: Yahoo Finance (consulted on Jan 10th, 2016)',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.02,
            bgcolor='#FFFFFF'  # white
        )]))
    return fig

def main(filename):
    top = 4

    stats = pd.read_csv(filename)

    top_sorted = get_most_popular('industry', stats, top)

    title = "Comparison of industries' returns and profitability."
    x_title = "Return on Assets %"
    y_title = "Profit Margin %"

    data = make_plotly_data(stats, top_sorted)

    layout = set_layout(x_title, y_title)

    fig = go.Figure(data=data, layout=layout)

    fig = hover_over_text(fig, stats, top_sorted)

    fig = add_data_source_note(fig)

    py.iplot(fig, filename='test')