#! /usr/bin/env python3

import os
import sys
import re

def buy_equal_ptf(cands, stock_states, money): #TODO fees
    ret = dict()
    cands = sorted(list(cands))
    if len(cands) == 0:
        return ret
    money_per_company = money / len(cands)
    for cand in cands:
        amount = int(money_per_company / stock_states[cand].close_price) // 100 * 100
        if amount >= 100:
            ret[cand] = (stock_states[cand].close_price, amount)
            money -= amount * stock_states[cand].close_price
    flag = True
    while flag:
        flag = False
        for cand in cands:
            this_money = stock_states[cand].close_price * 100
            if this_money < money:
                flag = True
                amount = 100
                if cand in ret:
                    amount = ret[cand][1] + 100
                ret[cand] = (stock_states[cand].close_price, amount)
                money -= this_money
    rm_cands = list()
    for key in ret:
        if ret[key][0] * ret[key][1] < 1000.0:
            rm_cands.append(key)
    for key in rm_cands:
        del ret[key]
    return ret