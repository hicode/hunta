#! /usr/bin/env python3

import os
import sys
import re


def nonneg_idx(idx):
    if idx < 0:
        return 0
    return idx

class day_struct:
    def __init__(self, name):
        self.name = name
        self.date = list()
        self.open_price = list()
        self.high_price = list()
        self.low_price = list()
        self.close_price = list()
        self.amount = list()
        self.volume = list()
        
    def put(self, date, open_price, high_price, low_price, close_price, amount, volume):
        idx = len(self.date)
        while idx - 1 >= 0 and self.date[idx - 1] > date:
            idx -= 1
        
        self.date.insert(idx, date)
        self.open_price.insert(idx, open_price)
        self.high_price.insert(idx, high_price)
        self.low_price.insert(idx, low_price)
        self.close_price.insert(idx, close_price)
        self.amount.insert(idx, amount)
        self.volume.insert(idx, volume)
    
    def latest(self):
        return len(self.date) - 1    
    
    def a(self, idx):
        return self.amount[nonneg_idx(idx)]
    def v(self, idx):
        return self.volume[nonneg_idx(idx)]
    def o(self, idx):
        return self.open_price[nonneg_idx(idx)]
    def l(self, idx):
        return self.low_price[nonneg_idx(idx)]
    def h(self, idx):
        return self.high_price[nonneg_idx(idx)]
    def c(self, idx):
        return self.close_price[nonneg_idx(idx)]
        
#tester
if __name__ == '__main__':
    pass