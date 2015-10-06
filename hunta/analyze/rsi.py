#! /usr/bin/env python3


import ..util.math

def calc_rsi(stock, period):
    return RSI(stock.close_price, period)