__author__ = 'Alexandre'

from yahoo_finance import Share


def parse_powers(x):
    powers = {'B': 10 ** 9, 'M': 10 ** 6, 'T': 10 ** 12}
    try:
        power = x[-1]
        return float(x[:-1]) * powers[power]
    except TypeError:
        return x


def get_key_stats(stock):
    try:
        mc = parse_powers(Share(stock).get_market_cap())
        pb = Share(stock).get_price_book()
        pe = Share(stock).get_price_earnings_ratio()

        return ['mc', 'pb', 'pe' ], [mc, pb, pe]

    except Exception,e :
        print 'failed in yahoo_key_stats for ', stock, ' ', str(e)


