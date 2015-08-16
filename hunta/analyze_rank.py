#! /usr/env/bin python

import os
import sys
import re


from .util.util import *
from .util.io import *
from .analyze import macd



stock_fn_list = day_list_tdx()

good_cands = list()

for stock_fn in stock_fn_list:
    stock = parse_tdx_day(stock_fn)
    if stock.date[-1] != last_trade_date():
        continue
    is_gc, cross_val = macd.gold_cross(stock, stock.latest())
    #is_gc, cross_val = macd.double_low_gold_cross(stock, stock.latest())
    if is_gc:
        #print stock.name
        good_cands.append((abs(cross_val), (stock.name, cross_val)))

sort_cands = sorted(good_cands, key=sort_key)

for cand in sort_cands:
    print cand[1]
