#! /usr/bin/env python


import ..util.math

def calc_rsi(stock, period):
    return RSI(stock.close_price, period)