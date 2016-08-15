#! /usr/bin/env python3

import os
import sys
import re

import numpy as np 
import talib

def rsi_overbuy_sign(hist, threshold = 80.0):
    rsi = talib.RSI(hist.close_price, 6)[-1]
    if rsi > threshold:
        return True
    return False

def macd_deadcross(hist):
    macd, macdsignal, macdhist = talib.MACD(hist.close_price, 12, 26, 9)
    
    if macd[-1] < macdsignal[-1] and macd[-2] > macdsignal[-2]:
        #plotter = stimu_plotter(100,range(100))
        #plotter.add_line(('macd', macd, []))
        #plotter.add_line(('macdsignal', macdsignal, []))
        #plotter.show()
        return True
    return False