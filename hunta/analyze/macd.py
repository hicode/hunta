#! /usr/bin/env python3

import sys
import os
import re

from ..util.math import *



def gold_cross(stock, date):
    if date - 1 < 0:
        return (False, None)
    
    diff = DIFF(stock.close_price)
    dea = DEA(stock.close_price)
    
    #print diff[date], diff[date - 1]
    #print dea[data], dea[date - 1]
    
    if diff[date - 1] < dea[date - 1] and diff[date] > dea[date]:
        cross_val = calc_cross_val(diff[date - 1], diff[date], dea[date - 1], dea[date])
        return (True, cross_val)
        
    return (False, None)


def double_low_gold_cross(stock, date, period = 13): #13 or 8
    is_gc, cross_val = gold_cross(stock, date)
    if not is_gc or is_gc and cross_val > 0:
        return (False, None)
    
    for old_date in range(date - 1, date - period, -1):
        is_old_gc, old_cross_val = gold_cross(stock, old_date)
        if is_old_gc:
            return (True, cross_val)

    return (False, None)
