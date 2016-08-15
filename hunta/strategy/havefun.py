#! /usr/bin/env python3


import os
import sys
import re

from ..sign import *
from .common import *

ext_resource = None

def gen_buy_cands(date, hist, valid_stock_idx):
    global ext_resource
    ret = set()
    
    cands = buy_tech_analysis.macd_goldcross_rank(hist, valid_stock_idx)
    
    for stock_idx in valid_stock_idx:
        my_hist = hist[stock_idx]
        #if buy_tech_analysis.rsi_oversold_sign(my_hist):
        #    ret.add(stock_idx)
        #if buy_tech_analysis.macd_goldcross(my_hist):
        #    ret.add(stock_idx)
        if buy_tech_analysis.macd_goldcross(my_hist):
            ret.add(stock_idx)
    return ret

def gen_sell_cands(date, hist, valid_stock_idx, cur_account):
    global ext_resource
    ret = set()
    for stock_idx in valid_stock_idx:
        if cur_account.stocks[stock_idx] == 0:
            continue
        my_hist = hist[stock_idx]
        if sell_general.gerou_sign(stock_idx, cur_account, my_hist):
            ret.add(stock_idx)
        if sell_general.luodaiweian_sign(stock_idx, cur_account, my_hist):
            ret.add(stock_idx)
        #if sell_tech_analysis.rsi_overbuy_sign(my_hist):
        #    ret.add(stock_idx)
        
        
        #if sell_tech_analysis.macd_deadcross(my_hist):
        #    ret.add(stock_idx)
        
    return ret