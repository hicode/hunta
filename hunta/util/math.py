#! /usr/bin/env python3


import os
import sys
import math
import re
import copy


EPS = 1e-6


def cut_hist_array(hist, length):
    if len(hist) >= length:
        return copy.copy(hist[len(hist) - length:])
    ret = list()
    
    for i in range(length - len(hist)):
        ret.append(hist[0])
    ret.extend(hist)
    
    return ret

def calc_cross_val(line1_y1, line1_y2, line2_y1, line2_y2):
    d_line1 = line1_y2 - line1_y1
    d_line2 = line2_y2 - line2_y1
    cross_val = (d_line2 * line1_y1 - d_line1 * line2_y1) / (d_line2 - d_line1)
    return cross_val

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

def RSI_oneday(hist):
    global EPS
    
    U = list()
    D = list()
    
    for i in range(1, len(hist)):
        diff = hist[i] - hist[i - 1]
        if diff > 0:
            U.append(abs(diff))
            D.append(0.0)
        else:
            U.append(0.0)
            D.append(abs(diff))
    ema_u = EMA(U, len(hist))[-1]
    ema_d = EMA(D, len(hist))[-1]
    
    if ema_u + ema_d < EPS:
        return 0.5
    else:
        return ema_u / (ema_u + ema_d)

def RSI(seq, period):
    ret = list()
    for i in range(1, len(seq)):
        ret.append(RSI_oneday(cut_hist_array(hist[:i], period)))
    return ret

