__author__ = 'Alexandre'

import urllib2


def float_or_none(x):
    try: return float(x)
    except: return None


def get_mc(source_code):
    mc = source_code.split(
        'Market Cap (intraday)<font '
        'size="-1"><sup>5</sup></font>:</td><td '
        'class="yfnc_tabledata1"><span id="yfs_j10_')[-1].split(
        '</span>')[0].split('>')[-1]
    if mc[-1] == 'B':
        return float_or_none(mc[:-1])*1000000000
    elif mc[-1] == 'M':
        return float_or_none(mc[:-1])*1000000
    else:
        return 0


def get_prm(source_code):
    prm = source_code.split(
        'Profit Margin (ttm):</td><td class="yfnc_tabledata1">')[-1].split(
        '%</td>')[0]
    return float_or_none(prm)


def get_roa(source_code):
    roa = source_code.split(
        'Return on Assets (ttm):</td><td class="yfnc_tabledata1">')[-1].split(
        '%</td>')[0]
    return float_or_none(roa)


def get_source_code(url):
    return urllib2.urlopen(url).read()


def yahoo_key_stats(stock):
    try:
        url = 'http://finance.yahoo.com/q/ks?s=' + stock
        source_code = get_source_code(url)

        mc = get_mc(source_code)
        prm = get_prm(source_code)
        roa = get_roa(source_code)

        return ['mc', 'prm', 'roa' ], [mc, prm, roa]

    except Exception,e :
        print 'failed in yahoo_key_stats ', str(e)


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