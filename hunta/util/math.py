#! /usr/bin/env python


import os
import sys
import math
import re


def vect_scale_add(seq1, seq2, scale1, scale2):
    if len(seq1) != len(seq2):
        raise Exception('Vector dimension mismatches.')
    ret = list()
    for i in range(len(seq1)):
        ret.append(scale1 * seq1[i] + scale2 * seq2[i])
    return ret

def EMA(seq, period, alpha = None):
    if alpha == None:
        alpha = 2.0 / (period + 1)
    ret = list()
    ret.append(seq[0])
    for i in range(1, len(seq)):
        ret.append(alpha * seq[i] + (1 - alpha) * ret[-1])
    return ret

    
def DIFF(seq, short_period = 12, long_period = 26):
    ema_short = EMA(seq, short_period)
    ema_long = EMA(seq, long_period)
    return vect_scale_add(ema_short, ema_long, 1, -1)
    
def DEA(seq, mid_period = 9):
    return EMA(DIFF(seq), mid_period)
    
def MACD(seq, short_period, long_period, mid_period):
    diff = DIFF(seq, short_period, long_period)
    dea = DEA(seq, mid_period)
    return vect_scale_add(diff, dea, 2, -2)
    
    
def sort_key(item, idx = 0):
    return item[idx]
    
def calc_cross_val(line1_y1, line1_y2, line2_y1, line2_y2):
    d_line1 = line1_y2 - line1_y1
    d_line2 = line2_y2 - line2_y1
    cross_val = (d_line2 * line1_y1 - d_line1 * line2_y1) / (d_line2 - d_line1)
    return cross_val