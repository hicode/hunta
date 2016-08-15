#! /usr/bin/env python3



import os
import sys
import re
from struct import *
import zipfile
import concurrent.futures


from .ds import *
from .util import *


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
        print(splits)

#tongdaxin
def parse_tdx_day(fn):
    name = os.path.basename(fn).split('.')[0]
    ret = stock_day_struct(name)
    
    tdx_file = open(fn, 'rb')
    buf = tdx_file.read()
    tdx_file.close()
    
    num = len(buf)
    no = num // 32
    b = 0
    e = 32
    
    for i in range(no):
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
    sh_dir = root + '/data/lday/shlday/'
    sz_dir = root + '/data/lday/szlday/'
    
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

def day_index_list_tdx(root = './'):
    sh_dir = root + '/data/lday/shlday/'
    sz_dir = root + '/data/lday/szlday/'
    
    ret = list()
    
    list_sh = os.listdir(sh_dir)
    for stock_id in list_sh:
        if not stock_id.startswith('sh00'):
            continue
        ret.append(sh_dir + stock_id)
        
    return ret
    
def day_dict_tdx(root = './'):
    lst = day_list_tdx(root)
    dct = dict()
    for stock in lst:
        dct[stock.rsplit('/')[-1].rsplit('.')[0]] = stock
    return dct

def day_index_dict_tdx(root = './'):
    lst = day_index_list_tdx(root)
    dct = dict()
    for stock in lst:
        dct[stock.rsplit('/')[-1].rsplit('.')[0]] = stock
    return dct
    
def get_one_market_tdx_day_source(root, download, addr):
    local_dir =  root + '/data/raw/'
    local_fn = local_dir + '/all.' + str(last_trade_date()) + '.' + addr.split('/')[-1]    
    print(local_fn, addr)
    if download:
        os.system('wget -O %s %s' % (local_fn, addr))
    
    zipf = zipfile.ZipFile(local_fn)
    to_dir = root + '/data/lday/' + addr.split('/')[-1].split('.')[0]
    zipf.extractall(to_dir)


def get_allhist_tdx_day_source(root = './', download = True):
    sh_addr = 'http://www.tdx.com.cn/products/data/data/vipdoc/shlday.zip'
    sz_addr = 'http://www.tdx.com.cn/products/data/data/vipdoc/szlday.zip'
    if not os.path.exists(root + '/data/raw'):
        os.makedirs(root + '/data/raw')
    if not os.path.exists(root + '/data/lday'):
        os.makedirs(root + '/data/lday')
    #pc = concurrent.futures.ThreadPoolExecutor(max_workers=2);
    #for addr in [sh_addr, sz_addr]:
    #    pc.submit(get_one_market_tdx_day_source, root, download, addr)
    #pc.shutdown() 
    joblist = [(root, True, sh_addr), (root, True, sz_addr)]
    run_array(2, get_one_market_tdx_day_source, joblist);
        
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
    #get_allhist_tdx_day_source()
    print(day_list_tdx())
    
