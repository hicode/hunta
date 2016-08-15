#! /usr/bin/env python3

from .stimulate.day_stimulator import *
from .util.io import *
from .plot.stimu_plotter import *

money = 100000
days = 100

all_stocks = day_dict_tdx()
all_index = day_index_dict_tdx()
stock1 = parse_tdx_day(all_stocks['sh601857'])
stock2 = parse_tdx_day(all_stocks['sh601988'])
index300 = parse_tdx_day(all_index['sh000300'])

hist1 = trace_index(money, stock1, days)
hist2 = trace_index(money, stock2, days)

hist_index300 = trace_index(money, index300, days)

hist1[2].extend([('buy',2,True),('buy',4,False),('sell',5,True),('sell',0,False)])

plotter = stimu_plotter(days)
plotter.add_line(hist1)
plotter.add_line(hist2)
plotter.add_line(hist_index300)
plotter.show()
