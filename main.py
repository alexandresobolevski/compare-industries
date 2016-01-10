__author__ = 'Alexandre'


import csv, time
from yahoo import get_sp500list, yahoo_key_stats
import pandas as pd
import random
import plotly.plotly as py
import plotly.tools as tls
from plotly import graph_objs as go
import collections


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


def yahoo_populate():
    tickers = get_sp500list()
    print tickers
    for ticker in tickers.keys():
        print ticker
        try:
            names, stats = yahoo_key_stats(ticker)
            time.sleep(.2)
            for name, stat in zip(names,stats):
                tickers[ticker][name] = stat
        except Exception, e:
            tickers.pop(ticker, None)
            print 'failed to save to dict the data', str(e)
    #{'AGN': {'insp': 88.4, 'roa': 1.7, 'name': 'Allergan plc','mc': 121710000000.0}

    print 'writing to file'
    writer = csv.writer(open('sp500.csv', 'wb'))
    writer.writerow(tickers[ticker].keys())
    for ticker in tickers:
        writer.writerow(tickers[ticker].values())

# yahoo_populate()

py.sign_in('sobolevski.a', '1gd9i51p36')

stocks = pd.read_csv('sp500.csv')
data = go.Data()
max_industries = 4
colors_array = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                '#9467bd']

industries_counted = collections.Counter(stocks['industry'])
industries_sorted = [(l,k) for k,l in sorted([(j,i) for i,j in industries_counted.items()], reverse=True)]
industries_sorted = [name for name,_ in industries_sorted]
industries_sorted = industries_sorted[:max_industries]
print industries_sorted

counter = 0
for industry, X in stocks.groupby('industry'):
    if counter > 4: break
    if industry in industries_sorted:
        counter +=1
        # print X
        sizes = X['mc']
        color = colors_array[counter-1]
        data.append(
            make_trace(X, sizes, industry, color))

title = "Comparison of industries' returns and profitability."
x_title = "Return on Assets %"
y_title = "Profit Margin %"

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
        range=[0,25]
    ),
    yaxis=go.YAxis(
        axis_style,
        title=y_title,
        range=[-10, 60]
    )
)

fig = go.Figure(data=data, layout=layout)

counter = 0
for industry, X in stocks.groupby('industry'):
    if industry in industries_sorted:
        text = X.apply(make_text, axis=1).tolist()
        fig['data'][counter].update(text=text)
        counter +=1

fig['layout'].update(annotations=go.Annotations([
    go.Annotation(
        text='Data source: Yahoo Finance (consulted on Jan 10th, 2016)',
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.98,
        y=0.02,
        bgcolor='#FFFFFF'    # white
    )]))

# py.iplot(fig, filename='SP500 sectors chart')