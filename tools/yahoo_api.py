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
        mc = float(parse_powers(Share(stock).get_market_cap()))
        pb = float(Share(stock).get_price_book())
        peg = float(Share(stock).get_price_earnings_growth_ratio())
        p = float(Share(stock).get_price())
        ph = float(Share(stock).get_historical('2016-01-19', '2016-01-19')[0]['Adj_Close'])
        r = (p - ph)/ph
        return ['mc', 'pb', 'peg', 'r'], [mc, pb, peg, r]

    except Exception,e :
        print 'failed in yahoo_key_stats for ', stock, ' ', str(e)
