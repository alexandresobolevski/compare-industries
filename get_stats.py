__author__ = 'Alexandre'


import csv, time
import bubble_chart
from yahoo_api import get_tickers_dict, yahoo_key_stats


def wait(seconds):
    time.sleep(seconds)


def write_stats(tickers, filename):
    print 'writing to file...'
    writer = csv.writer(open(filename, 'wb'))
    # write headers
    writer.writerow(dict.keys()[0].keys())
    for ticker in tickers:
        writer.writerow(tickers[ticker].values())


def get_stats_for(tickers):
    for ticker in tickers.keys():
        print 'getting stats for ', ticker
        try:
            names, stats = yahoo_key_stats(ticker)
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


def main():

    filename = 'sp500.txt'

    tickers = get_tickers_dict(filename)

    tickers = get_stats_for(tickers)

    write_stats(tickers, filename)

    bubble_chart(filename)


if __name__ == "__main__":
    main()
