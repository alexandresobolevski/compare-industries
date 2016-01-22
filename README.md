# compare industries

## What it does

Creates a plot.ly based interactable plot that eases the search
for undervalued companies (using price/book and
price/earnings/growth). A potentially undervalued company would
situate itself within the box delimited by (0,0), (1,0), (1,1) and
(0,1).

Copmanies copmared are those in the sp500.txt. The file can be
replaced for another list with same format. See below for instructions.

Uses an available package from github to interface with yahoo/finance
 developed by lukaszbanasiak (https://github
 .com/lukaszbanasiak/yahoo-finance).

See example of result (here)[https://plot.ly/~sobolevski.a/45/value-investing-strategy/].

## Installation

Get an account for [plotly](https://plot.ly). Replace credentials
.json.example file with your own.

Install yahoo_finance by lukaszbanasiak.
```
pip install yahoo-finance
```

## To use

Run get_stats.py. Update sp500.txt or use another file and update
parameter filename in get_stats.py.

If new file instead of sp500.txt, change the variable FILENAME in
main.py.