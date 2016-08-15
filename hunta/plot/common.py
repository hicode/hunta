#! /usr/bin/env python3


import os
import sys
import re
import math


import matplotlib.pyplot as plt

def refine_x_axis(plt, xmin, xmax, tickers, num_xticker = 10):
    plt.xlim([xmin, xmax])
    xtk_steps = math.ceil((xmax - xmin) / num_xticker)
    now_tk = 0
    tk_pos = list()
    tk = list()
    while now_tk <= xmax - 1:
        tk.append(tickers[now_tk])
        tk_pos.append(now_tk)
        now_tk += xtk_steps
    tk.append(tickers[-1])
    tk_pos.append(xmax)
    plt.xticks(tk_pos, tk, rotation=45)