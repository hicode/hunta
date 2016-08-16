#! /usr/bin/env python3

import os
import sys


def crisis_sign(index_hist, threshold = 0.07, duration=20):
    close_price_hist = index_hist.close_price[-duration:]
    max_val = max(close_price_hist)
    if close_price_hist[-1]  / max_val <= 1 - threshold:
        #print('gegeda', close_price_hist[-1], max_val, index_hist.date[-1])
        return True
    #for i in range(len(close_price_hist)-2):
    #    if close_price_hist[i] > close_price_hist[i + 1] and close_price_hist[i + 1] > close_price_hist[i + 2] and close_price_hist[i + 2] / close_price_hist[i] <= 1.0 - threshold:
    #        return True
    return False