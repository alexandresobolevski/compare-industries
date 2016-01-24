__author__ = 'Alexandre'

import pandas as pd
import plotly.plotly as py
import collections
import json
from plotly import graph_objs as go


def make_text(X):
    print X
    return 'Company: %s\
    <br>Price to book: %s \
    <br>Price to earnings growth: %s \
    <br>Market Cap: %s $B'\
    % (X['name'], X['pb'], X['peg'], X['mc']/1000000000)


def make_trace(frame, sizes, segments, colors):
    X = frame.to_dict('list')
    sizeref = (sizes.max() / 1e2 ** 2)*4
    return go.Scatter(
        x=X['pb'],
        y=X['peg'],
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
                    '#9467bd', '#ffa64d', '#008000', '#663400',
                    '#00cccc', '#6600cc']
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


def set_layout(title, x_title, y_title):
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
        height=700,
        hovermode='closest',
        xaxis=go.XAxis(
            axis_style,
            title=x_title,
            range=[0, 2]
        ),
        yaxis=go.YAxis(
            axis_style,
            title=y_title,
            range=[0, 2]
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
            text='Data source: Yahoo Finance (consulted on Jan 19th, '
                 '2016)',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.98,
            y=0.02,
            bgcolor='#FFFFFF'  # white
        )]))
    return fig


def bubble_chart(filename):
    with open('tools/plotly_credentials.json', 'r') as creds:
        credentials = json.load(creds)

    py.sign_in(credentials['plotly']['username'],
               credentials['plotly']['key'])
    # plot top industries (selected by market cap), make sure
    # enough to colors in colors_array of make_plotly_data fun
    top = 10

    stats = pd.read_csv(filename)

    top_sorted = get_most_popular('industry', stats, top)

    title = "Value Investing Strategy (find companies with pb <1 and peg <1)."
    x_title = "Price/Book Value"
    y_title = "Price/Earnings/Growth"
    data = make_plotly_data(stats, top_sorted)

    layout = set_layout(title, x_title, y_title)

    fig = go.Figure(data=data, layout=layout)

    fig = hover_over_text(fig, stats, top_sorted)

    fig = add_data_source_note(fig)

    py.iplot(fig, filename='SP500')
