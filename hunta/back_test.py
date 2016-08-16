#! /usr/bin/env python3

import os
import re
import sys


from .stimulate.epoch_stimulator import *
from .util.io import *
from .plot.stimulate_plot import *
from .util.ds import *

#specify strategy
from .strategy.havefun import *
from .strategy.common import *

#load external resource
ext_resource = None

money = 100000
days = 150

all_stocks = day_dict_tdx()
all_index = day_index_dict_tdx()
stimulator = epoch_stimulator(money, days)
cnt = 0

stimulator.add_index(parse_tdx_day(all_index['sh000001'])) #used to trace time

stk_stimu = 'sh600030'

for stock in sorted(all_stocks.keys()):
    stimulator.add_stock(parse_tdx_day(all_stocks[stock]))
    cnt += 1
    if cnt > 50:
        break
        pass
hist = stimulator.retrieve_stock_history_np()
hist_index = stimulator.retrieve_index_history_np()


while not stimulator.finish():
    now_state = stimulator.now_state()
    cur_account = stimulator.account
    cur_stocks = now_state.stocks
    cur_index = now_state.index
    #update price history
    for stock_idx in cur_stocks:
        hist[stock_idx].update(cur_stocks[stock_idx])
    for idx in stimulator.index:
        hist_index[idx].update(cur_index[idx])
    #print(hist_index['sh000001'].close_price)
    #gen buy_cands
    buy_cands = gen_buy_cands(now_state.date, hist, hist_index, now_state.valid_stock_idx, cur_account)
    #gen sell_cands
    sell_cands = gen_sell_cands(now_state.date, hist, hist_index, now_state.valid_stock_idx, cur_account)
    #refine_buy
    buy_cands.difference_update(sell_cands)
    #do sell
    for cand in sell_cands:
        stimulator.sell(cand, cur_stocks[cand].close_price, cur_account.stocks[cand])
    #gen_portfolio_buy
    buy_ptf = buy_equal_ptf(buy_cands, cur_stocks, cur_account.money)
    #do buy
    for cand in sorted(buy_ptf.keys()):
        stimulator.buy(cand, buy_ptf[cand][0], buy_ptf[cand][1])
    stimulator.next()


my_profile = stimulator.profile_data
my = ('my', my_profile.nav_hist, stimulator.profile_data.actions)
#my = ('my', my_profile.nav_hist, [])
stimulator.print_profile()
print('return=%.2f' %((stimulator.profile_data.return_hist[-1] - 1.0) * 100))



index300 = parse_tdx_day(all_index['sh000300'])
trace_index300 = trace_index(money, index300, days)

indexsha = parse_tdx_day(all_index['sh000001'])
trace_indexsha = trace_index(money, indexsha, days)

indexszc = parse_tdx_day(all_index['sz399001'])
trace_indexszc = trace_index(money, indexszc, days)


indexstock = parse_tdx_day(all_stocks[stk_stimu])
trace_indexstock = trace_index(money, indexstock, days)

plotter = stimu_plotter(days, my_profile.dates)
plotter.add_line(my)
plotter.add_line(trace_index300)
plotter.add_line(trace_indexsha)
plotter.add_line(trace_indexszc)
plotter.add_line(trace_indexstock)
plotter.show()

