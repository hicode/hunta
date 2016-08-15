#! /usr/bin/env python3

import os
import sys
import re
import math

import matplotlib.pyplot as plt

from .common import *

def two_curve(curve1, curve2, x, name_curve1 = 'line1', name_curve2 = 'line2', anchors=[]):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(curve1, color='b')
    ax2 = ax1.twinx()
    ax2.plot(curve2, color='r')
    refine_x_axis(plt, 0, len(curve1) - 1, x)
    for anchor in anchors:
        plt.axvline(x=anchor, ls='dotted')
    plt.show()