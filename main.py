__author__ = 'Alexandre'

import csv
import time
from tools.bubble_chart import bubble_chart
from tools.yahoo_api import get_key_stats


def wait(seconds):
    time.sleep(seconds)


def write_stats(tickers, filename):
    print 'writing to file...'
    writer = csv.writer(open(filename, 'wb'))
    # write headers
    writer.writerow(tickers[tickers.keys()[0]].keys())
    for ticker in tickers:
        writer.writerow(tickers[ticker].values())


def get_stats_for(tickers):
    for ticker in tickers.keys():
        print 'getting stats for ', ticker
        try:
            names, stats = get_key_stats(ticker)
            wait(0.2) # being a good citizen
            for name, stat in zip(names,stats):
                tickers[ticker][name] = stat
        # keep ticker stats only if all stats are valid
        except Exception, e:
            tickers.pop(ticker, None)
            print 'failed to save to dict ', str(e)
    # example of tickers {'AGN':
    # {'prm': 88.4, 'roa': 1.7, 'name': 'Allergan plc','mc': 121710000000.0}
    return tickers


def get_tickers_dict(filename):
    tickers = {}
    try:
        f = open(filename,'r').read()
        split_file = f.split('\n')
        for line in split_file:
            split_line = line.split(',')
            tickers[split_line[0]] = {'name': split_line[1],'industry': split_line[2]}
        return tickers
    except Exception, e:
        print 'failed in get_tickers_dict', str(e)


def main():

    filename = 'sp500'

    # tickers = get_tickers_dict(filename + '.txt')
    #
    # tickers = get_stats_for(tickers)
    #
    # write_stats(tickers, filename + '.csv')

    bubble_chart(filename + '.csv')


if __name__ == "__main__":
    main()
