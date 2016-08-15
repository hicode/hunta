#! /usr/bin/env python3

import os
import re
import sys


from ..stimulate.epoch_stimulator import *
from ..util.io import *
from ..plot.stimulate_plot import *
from ..util.ds import *


def retrieve_hist():
    money = 0
    days = 1
    all_stocks = day_dict_tdx()
    all_index = day_index_dict_tdx()
    stimulator = epoch_stimulator(money, days)
    cnt = 0
    stimulator.add_index(parse_tdx_day(all_index['sh000001'])) #used to trace time
    for stock in sorted(all_stocks.keys()):
        stimulator.add_stock(parse_tdx_day(all_stocks[stock]))
        cnt += 1
        if cnt > 100:
            break
            pass
    hist = stimulator.retrieve_stock_history_np()
    now_state = stimulator.now_state()
    return (now_state.valid_stock_idx, hist)
