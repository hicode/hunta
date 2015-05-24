#! /usr/bin/env python



import os
import sys
import re
from struct import *


from .ds import *
from .math import *

#tonghuashun TODO prices failed to parse ???
def parse_ths_day(fn):
    name = os.path.basename(fn).split('.')[0]
    ret = day_struct(name)
    
    fp = open(fn, 'rb')
    buf = fp.read()
    fp.close()

    
    skip_len, len_per_item, col_per_item  = unpack('HHH', buf[10:10+6])
    
    #print skip_len, len_per_item, col_per_item
    
    for now_ptr in range(skip_len, len(buf), len_per_item):
        splits = unpack('IHHHHHHHHII'  + 'I' * (col_per_item - 7), buf[now_ptr:now_ptr + len_per_item])
        print splits

#tongdaxin
def parse_tdx_day(fn):
    name = os.path.basename(fn).split('.')[0]
    ret = day_struct(name)
    
    tdx_file = open(fn, 'rb')
    buf = tdx_file.read()
    tdx_file.close()
    
    num = len(buf)
    no = num / 32
    b = 0
    e = 32
    
    for i in xrange(no):
        splits = unpack('IIIIIfII', buf[b:e])

        date = splits[0]
        open_price = splits[1] / 100.0
        high_price = splits[2] / 100.0
        low_price = splits[3] / 100.0
        close_price = splits[4] / 100.0
        amount = splits[5] / 10000.0
        volume = splits[6] / 100.0
        #reserved = splits[7]
        
        #print date, open_price, high_price, low_price, close_price, amount, volume
        #exit(0)
        ret.put(date, open_price, high_price, low_price, close_price, amount, volume)
        
        b += 32
        e += 32
    
    return ret

    
def day_list_tdx(root = './'):
    sh_dir = root + '/data/shlday/'
    sz_dir = root + '/data/szlday/'
    
    ret = list()
    
    list_sh = os.listdir(sh_dir)
    for stock_id in list_sh:
        if not stock_id.startswith('sh60'):
            continue
        ret.append(sh_dir + stock_id)
        
    list_sz = os.listdir(sz_dir)
    for stock_id in list_sz:
        if not stock_id.startswith('sz00') and not stock_id.startswith('sz30'):
            continue
        ret.append(sz_dir + stock_id)
    
    return ret
        
#tester
if __name__ == '__main__':
    pass
    #parse_ths_day('D:\\htzqzyb2\\history\\shase\\day\\600519.day')
    #stock = parse_tdx_day('D:\\proj\\hunta\\data\\shlday\\sh601318.day')
    #print stock.name
    #idx = stock.latest()
    #print stock.date[idx], stock.open_price[idx], stock.low_price[idx], stock.high_price[idx], stock.close_price[idx], stock.volume[idx], stock.amount[idx]
    #diff = DIFF(stock.close_price)
    #dea = DEA(stock.close_price)
    #for i in range(len(diff) - 30, len(diff)):
    #    print diff[i], ',' ,
    #
    #print ''
    #
    #for i in range(len(diff) - 30, len(diff)):
    #    print dea[i], ',' ,
    print day_list_tdx()
    