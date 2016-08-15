#! /usr/bin/env python3

import sys
import os
import re
import time
from datetime import datetime
from datetime import date
import zipfile
import concurrent.futures


def floor_money(money):
    return int(money * 100) / 100

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
    
def is_stock_delisted(stock):
    last_date = stock.date[-1]
    last_date_dt = date(last_date // 10000, last_date % 10000 // 100, last_date % 100)
    now = last_trade_date()
    now_dt = date(now // 10000, now % 10000 // 100, now % 100)
    diff = now_dt - last_date_dt
    if diff.days > 20:
        return True
    return False

def run_array(num_worker, func, job_array):
    ret = list()
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=num_worker)
    #for res in executor.map(func, *job_array):
    #    if res != None:
    #        ret.append(res)
    fut_lst = list()
    for args in job_array:
        if isinstance(args, (list, tuple)):
            future = executor.submit(func, *args)
        else:
            future = executor.submit(func, args)
        fut_lst.append(future)
        
    for future in fut_lst:
        res = future.result()
        if res != None:
            ret.append(res)
    return ret

if __name__ == '__main__':
    pass
