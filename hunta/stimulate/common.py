#! /usr/bin/env python3

import os
import re
import sys
import copy


class stimu_state():
    def __init__(self, account, stocks, index, date, valid_stock_idx):
        self.account = copy.deepcopy(account)
        self.stocks = stocks
        self.date = date
        self.valid_stock_idx = sorted(list(valid_stock_idx))
        self.index = index
        
class stimu_accont():
    def __init__(self, money):
        self.money = money
        self.stocks = dict()
        self.stocks_money = dict()
        self.stocks_valid_price = dict()
    
    def now_nav(self):
        ret = self.money
        for stock in self.stocks:
            if self.stocks[stock] > 0:
                ret += self.stocks[stock] * self.stocks_valid_price[stock]
        return ret
    
class stimu_profile():
    def __init__(self, init_money):
        self.transactions = list()
        self.actions = list()
        self.states = list()
        self.dates = list()
        
        self.init_money = init_money
        self.nav_hist = list()
        self.return_hist = list()
        
    def add_nav(self, nav):
        self.nav_hist.append(nav)
        self.return_hist.append(nav / self.init_money)
        
    def add_journal(self, act, trans):
        self.transactions.append(trans)
        self.actions.append(act)
    def add_state(self, state):
        self.states.append(state)
        self.dates.append(state.date)
    
    

class stimu_journal_item():
    def __init__(self, epoch, act, stock, act_price, act_amount, trans_price, trans_amount):
        self.epoch = epoch
        self.act = act
        self.stock = stock
        self.act_price = act_price
        self.act_amount = act_amount
        self.trans_price = trans_price
        self.trans_amount = trans_amount

class stimu_action():
    def __init__(self, act, stock_idx, price, amount):
        self.act = act
        self.stock_idx = stock_idx
        self.price = price
        self.amount = amount
class buy_action(stimu_action):
    def __init__(self, stock_idx, price, amount):
        stimu_action.__init__(self, 'buy', stock_idx, price, amount)
class sell_action(stimu_action):
    def __init__(self, stock_idx, price, amount):
        stimu_action.__init__(self, 'sell', stock_idx, price, amount)
class naive_action(stimu_action):
    def __init__(self, stock_idx, price, amount):
        stimu_action.__init__(self, 'naive', stock_idx, price, amount)
