#! /usr/bin/env python3

import os
import sys
import re
import math

import numpy as np 
import talib

from ..plot.analyse_plot import *

def rsi_oversold_sign(hist, threshold = 20.0):
    rsi = talib.RSI(hist.close_price, 6)[-1]
    if rsi < threshold:
        return True
    return False

    
def sork_key_2nd(item):
    return item[1]
def calc_cross_val(line1_y1, line1_y2, line2_y1, line2_y2):
    d_line1 = line1_y2 - line1_y1
    d_line2 = line2_y2 - line2_y1
    cross_val = (d_line2 * line1_y1 - d_line1 * line2_y1) / (d_line2 - d_line1)
    return cross_val
def macd_goldcross_rank(hists, valid_idx, num_top=5):
    ret = list()
    for stock in valid_idx:
        hist = hists[stock]
        macd, macdsignal, macdhist = talib.MACD(hist.close_price, 12, 26, 9)
        if macd[-1] > macdsignal[-1] and macd[-2] < macdsignal[-2]:
            #print(macd[-2], macd[-1])
            #print(macd[-5:])
            cross_val = calc_cross_val(macd[-2], macd[-1], macdsignal[-2], macdsignal[-1])
            #curve([macd[-20:], macdsignal[-20:]], hists[stock].date[-20:])
            ret.append((stock, abs(cross_val)))
    ret = sorted(ret, key=sork_key_2nd)
    if len(ret) > num_top:
        ret = ret[:num_top]
    ret_keys = list()
    for key, val in ret:
        ret_keys.append(key)
    return ret_keys
def macd_goldcross(hist):
    macd, macdsignal, macdhist = talib.MACD(hist.close_price, 12, 26, 9)
    
    if macd[-1] > macdsignal[-1] and macd[-2] < macdsignal[-2]:
        #plotter = stimu_plotter(100,range(100))
        #plotter.add_line(('macd', macd, []))
        #plotter.add_line(('macdsignal', macdsignal, []))
        #plotter.show()
        return True
    return False
    #elif macd[-1] < macdsignal[-1] and macd[-2] > macdsignal[-2]:
    #    #if amount <= 0:
    #    #    return None
    #    return sell_action(hist.name, hist.close_price[-1], amount)
    #return None