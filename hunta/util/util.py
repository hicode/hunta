#! /usr/bin/env python

import sys
import os
import re
import time
from datetime import datetime
import zipfile


def last_trade_date():
    if  hasattr(last_trade_date, "ret"):
        return last_trade_date.ret
    
    local_time = time.time()
    bj_time = local_time + time.timezone + 8 * 3600
    bj_time_before_trade =  bj_time - 15 * 3600
    dt = datetime.fromtimestamp(bj_time_before_trade)
    weekend_offset = 0
    if dt.weekday() == 6 or dt.weekday() == 5:
        weekend_offset = (dt.weekday() - 4) * 24 * 3600
    
    dt = datetime.fromtimestamp(bj_time_before_trade - weekend_offset)

    last_trade_date.ret = int(dt.strftime('%Y%m%d'))
    return last_trade_date.ret
    
    
def sort_key(item, idx = 0):
    return item[idx]
    
    
def day_list_tdx(root = './'):
    sh_dir = root + '/data/'
    sz_dir = root + '/data/'
    
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

def get_allhist_tdx_day_source(root = './', download = True):
    sh_addr = 'http://www.tdx.com.cn/products/data/data/vipdoc/shlday.zip'
    sz_addr = 'http://www.tdx.com.cn/products/data/data/vipdoc/szlday.zip'
    
    for addr in [sh_addr, sz_addr]:
        local_dir =  root + '/data/raw/'
        local_fn = local_dir + '/all.' + str(last_trade_date()) + '.' + addr.split('/')[-1]
        if download:
            os.system('wget -O %s %s' % (local_fn, addr))
        
        zipf = zipfile.ZipFile(local_fn)
        to_dir = root + '/data/' + addr.split('/')[-1].split('.')[0]
        zipf.extractall(to_dir)        

if __name__ == '__main__':
    get_allhist_tdx_day_source()