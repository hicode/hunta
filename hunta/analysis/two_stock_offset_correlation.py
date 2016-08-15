#! /usr/bin/env python3

import os
import re
import sys
import math

import numpy as np

from ..plot.analyse_plot import *
from .common import *

def search_key(itm):
    return abs(itm[0])

valid_idx, hist = retrieve_hist()

offset = 5
duration = 30

rank_lst = list()

for i in range(len(valid_idx)):
    if len(hist[valid_idx[i]].close_price) < duration + offset:
        continue
    for j in range(len(valid_idx)):
        if i == j:
            continue
        if len(hist[valid_idx[j]].close_price) < duration + offset:
            continue
        price_one = hist[valid_idx[i]].close_price[-duration-offset-1:-1-offset]
        price_two = hist[valid_idx[j]].close_price[-duration-1:-1]
        
        mean_one = np.mean(price_one)
        mean_two = np.mean(price_two)
        
        num = 0
        den1 = 0
        den2 = 0
        for k in range(len(price_one)):
            den1 += pow(price_one[k] - mean_one, 2)
            den2 += pow(price_two[k] - mean_two, 2)
            num += (price_one[k] - mean_one) * (price_two[k] - mean_two)
        r = num / math.sqrt(den1 * den2)
        rank_lst.append((r, valid_idx[i], valid_idx[j]))
rank_lst = sorted(rank_lst, key=search_key, reverse=True)[:10]
print(rank_lst)

for val, idx1, idx2 in rank_lst:
    dates = hist[idx1].date[-duration-offset-1:-1]
    price_one = hist[idx1].close_price[-duration-offset-1:-1]
    price_two = hist[idx2].close_price[-duration-1:-1]
    #if val < 0:
    #    price_two *= -1.0
    two_curve(price_one, price_two, dates, anchors=[duration-1])
    
    
    