#! /usr/bin/env python3

import os
import sys
import re
import copy

import numpy as np

class stock_epoch():
    def __init__(self, name, date, open_price, close_price, high_price, low_price, amount, volume):
        self.name = name
        self.date = date
        self.open_price = open_price
        self.close_price = close_price
        self.high_price = high_price
        self.low_price = low_price
        self.amount = amount
        self.volume = volume

class stock_day_struct:
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
    
    def history(self, offset_from_last):
        ret = stock_day_struct(self.name)
        if offset_from_last > len(self.date):
            return ret
        ret.date.extend(self.date[:-offset_from_last])
        ret.open_price.extend(self.open_price[:-offset_from_last])
        ret.high_price.extend(self.high_price[:-offset_from_last])
        ret.low_price.extend(self.low_price[:-offset_from_last])
        ret.close_price.extend(self.close_price[:-offset_from_last])
        ret.amount.extend(self.amount[:-offset_from_last])
        ret.volume.extend(self.volume[:-offset_from_last])
        return ret
    
    def update(self, a_stock_epoch):
        if a_stock_epoch.date == self.date[-1]:
            return
        self.date.append(a_stock_epoch.date)
        self.open_price.append(a_stock_epoch.open_price)
        self.high_price.append(a_stock_epoch.high_price)
        self.low_price.append(a_stock_epoch.low_price)
        self.close_price.append(a_stock_epoch.close_price)
        self.amount.append(a_stock_epoch.amount)
        self.volume.append(a_stock_epoch.volume)
        
class stock_day_struct_np:
    def __init__(self, raw_struct):
        self.name = raw_struct.name
        self.date = copy.copy(raw_struct.date)
        self.open_price = np.asarray(raw_struct.open_price)
        self.high_price = np.asarray(raw_struct.high_price)
        self.low_price = np.asarray(raw_struct.low_price)
        self.close_price = np.asarray(raw_struct.close_price)
        self.amount = np.asarray(raw_struct.amount)
        self.volume = np.asarray(raw_struct.volume)
    
    
    
    #TODO better options instead of array copy?    
    def talib_format(self):
        return {'open':self.open_price, 'close':self.close_price, 'high':self.high_price, 'low':self.low_price, 'volume':self.volume}
    def update(self, a_stock_epoch):
        if len(self.date) != 0 and a_stock_epoch.date == self.date[-1]:
            return
        self.date.append(a_stock_epoch.date)
        self.open_price = np.append(self.open_price, [a_stock_epoch.open_price])
        self.high_price = np.append(self.high_price, [a_stock_epoch.high_price])
        self.low_price = np.append(self.low_price, [a_stock_epoch.low_price])
        self.close_price = np.append(self.close_price, [a_stock_epoch.close_price])
        self.amount = np.append(self.amount, [a_stock_epoch.amount])
        self.volume = np.append(self.volume, [a_stock_epoch.volume])
#tester
if __name__ == '__main__':
    pass