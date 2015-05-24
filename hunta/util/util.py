#! /usr/bin/env python

import sys
import os
import re
import time
from datetime import datetime


def last_trade_date():
    if  hasattr(last_trade_date, "ret"):
        return last_trade_date.ret
    
    local_time = time.time()
    bj_time = local_time + time.timezone + 8 * 3600
    bj_time_before_trade =  bj_time - 9 * 3600
    dt = datetime.fromtimestamp(bj_time_before_trade)
    weekend_offset = 0
    if dt.weekday() == 6 or dt.weekday() == 5:
        weekend_offset = (dt.weekday() - 4) * 24 * 3600
    
    dt = datetime.fromtimestamp(bj_time_before_trade - weekend_offset)

    last_trade_date.ret = int(dt.strftime('%Y%m%d'))
    return last_trade_date.ret