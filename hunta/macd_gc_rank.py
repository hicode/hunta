#! /usr/env/bin python3

import os
import sys
import re


from .util.util import *
from .util.io import *
from .analyze import macd

def macd_gc(stock_fn):
    stock = parse_tdx_day(stock_fn)
    if is_stock_delisted(stock):
        return
    is_gc, cross_val = macd.gold_cross(stock, stock.latest())
    #is_gc, cross_val = macd.double_low_gold_cross(stock, stock.latest())
    if is_gc:
        return (abs(cross_val), (stock.name, cross_val))


def main():
    num_worker = 4
    if len(sys.argv) >= 2:
        num_worker = int(sys.argv[1])
    
    
    stock_fn_list = day_list_tdx()
    
    good_cands = run_array(num_worker, macd_gc, stock_fn_list)
    
    sort_cands = sorted(good_cands, key=sort_key)
    
    for cand in sort_cands:
        print(cand[1])


if __name__ == '__main__':
    main()
