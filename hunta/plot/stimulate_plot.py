#! /usr/bin/env python3

import os
import sys
import re
import math

import matplotlib.pyplot as plt

from .common import *

class stimu_plotter():
    def __init__(self, epochs, dates):
        self.epochs = epochs
        self.lines = list()
        self.dates = dates
    def add_line(self,line):
        self.lines.append(line)
    def show(self, show_marker=True, mksize=10, xmin=-1, xmax=-1, num_xticker = 10):
        fig = plt.figure()
        ax = fig.add_subplot(111)
    
        for line in self.lines:
            ax.plot(line[1], label=line[0], marker='.')
        if xmax == -1:
            xmax = self.epochs - 1
        if xmin == -1:
            xmin = 0
        
        
        refine_x_axis(plt, xmin, xmax, self.dates)
        
        ax.legend(loc='best')
        if show_marker:
            for line in self.lines:
                actions = line[2]
                for action in actions:
                    act = action[0]
                    pos = action[1]
                    succ = action[2]
                    co = 'g' # success
                    mk = '^' # buy
                    if act != 'buy':
                        mk = 'v' 
                    if not succ:
                        co = 'r'
                    #print(co)
                    ax.plot(pos, line[1][pos], marker=mk, color=co,markersize=mksize)
        
        
        
        
        plt.show()