import os
import re
import sys
import copy

from ..util.fee import *
from ..util.ds import *
from .common import *

def trace_index(money, stock, epochs):
    stock_idx = stock.name
    stimu = epoch_stimulator(money, epochs)
    stimu.add_stock(stock)
    state = stimu.now_state()
    cur_price = state.stocks[stock_idx].close_price
    #print(money / cur_price)
    stimu.next([naive_action(stock_idx, cur_price, money / cur_price)])
    while not stimu.finish():
        stimu.next([])
    return (stock_idx, stimu.profile_data.nav_hist, [])


    
def find_today_idx(date, date_lst, default_value):
    ret = default_value
    try:
        ret = date_lst.index(date)
    except Exception:
        pass
    return ret

class epoch_stimulator():
    def __init__(self, money, epochs):
        self.stocks = dict()
        self.account = stimu_accont(money)
        self.virtual_accounts = list()
        self.epoch_offset = epochs
        self.tot_epochs = epochs

        self.index = dict()
        
        self.profile_data = stimu_profile(money)
        
        self.not_finish = True
        
        self.today = None
    
    def add_index(self, index):
        self.index[index.name] = index
    
    def add_stock(self, stock):
        if 'sh000001' in self.index and stock.date[-1] != self.index['sh000001'].date[-1]:
            print('[WARN] %s is closed or delisted.' % (stock.name))
            return
        if len(stock.date) < self.tot_epochs:
            print('[WARN] %s is too new to include.' % (stock.name))
            return
        self.stocks[stock.name] = stock
        self.account.stocks[stock.name] = 0
        self.account.stocks_money[stock.name] = 0

    def print_profile(self):
        marco = 'Epoch%d[%s][%s,%.2f,%.2f][money_%.2f,amount_%d]: Act=%s_%d@%.2f, Trans=%d@%.2f, %s'
        for i in range(len(self.profile_data.actions)):
            tran_item = self.profile_data.transactions[i]
            act_item = self.profile_data.actions[i]
            act = tran_item[0]
            epoch = tran_item[1]
            succ = 'Succeed'
            if not tran_item[2]:
                succ = 'Failed'
            stock_idx = tran_item[3]
            tran_price = tran_item[4]
            tran_amount = tran_item[5]
            act_price = act_item[4]
            act_amount = act_item[5]

            high_price = self.stocks[stock_idx].high_price[-self.tot_epochs + epoch]
            low_price = self.stocks[stock_idx].low_price[-self.tot_epochs + epoch]

            ava_money = self.profile_data.states[epoch].account.money
            ava_amount = self.profile_data.states[epoch].account.stocks[stock_idx]
            
            date = self.profile_data.dates[epoch]
            
            print(marco % (epoch, date, stock_idx, low_price, high_price, ava_money, ava_amount, act, act_amount, act_price, tran_amount, tran_price, succ))

    def finish(self):
        ret = self.epoch_offset <= 1
        if ret:
            if self.not_finish:
                self.profile_data.add_nav(self.account.now_nav())
                self.profile_data.add_state(self.now_state())
                self.not_finish = False
        return ret
    
    
    def retrieve_index_history(self):
        ret = dict()
        for stock in self.index:
            ret[stock] = self.index[stock].history(self.epoch_offset)
        return ret

    def retrieve_index_history_np(self):
        raw_hist = self.retrieve_index_history()
        ret = dict()
        for stock in raw_hist:
            ret[stock] = stock_day_struct_np(raw_hist[stock])
        return ret
    
    def retrieve_stock_history(self):
        ret = dict()
        for stock in self.stocks:
            ret[stock] = self.stocks[stock].history(self.epoch_offset)
        return ret

    def retrieve_stock_history_np(self):
        raw_hist = self.retrieve_stock_history()
        ret = dict()
        for stock in raw_hist:
            ret[stock] = stock_day_struct_np(raw_hist[stock])
        return ret

    def now_state(self):
        #acc = copy.deepcopy(self.account)
        acc = self.account
        sto = dict()
        valid_sto_idx = set()

        if 'sh000001' in self.index:
            self.today = self.index['sh000001'].date[-self.epoch_offset]
        else:
            self.today = None
        #print(date)
        idx_dct = dict()
        for idx in self.index:
            epochid = -self.epoch_offset
            stock = self.index[idx]
            idx_dct[idx] = stock_epoch(stock.name, stock.date[epochid], stock.open_price[epochid], stock.close_price[epochid], stock.high_price[epochid], stock.low_price[epochid], stock.amount[epochid], stock.volume[epochid])
        for stock_idx in self.stocks:
            stock = self.stocks[stock_idx]
            
            if self.today == None:
                self.today = stock.date[-self.epoch_offset]
                
            epochid = find_today_idx(self.today, stock.date, -self.epoch_offset)
            sto[stock_idx] = stock_epoch(stock.name, stock.date[epochid], stock.open_price[epochid], stock.close_price[epochid], stock.high_price[epochid], stock.low_price[epochid], stock.amount[epochid], stock.volume[epochid])
            #print( sto[stock_idx].close_price )
            if self.today == sto[stock_idx].date and sto[stock_idx].volume != 0:
                valid_sto_idx.add(stock_idx)
                self.account.stocks_valid_price[stock_idx] = sto[stock_idx].close_price
                #exit(0)
        return stimu_state(acc, sto, idx_dct, self.today, valid_sto_idx)

    def next(self, actions = []):
        if self.finish():
            return
        self.profile_data.add_nav(self.account.now_nav())
        self.profile_data.add_state(self.now_state())
        self.epoch_offset -= 1
        for action in actions:
            my_act = action.act
            my_stock = action.stock_idx
            my_amount = int(action.amount)
            my_price = float(action.price)
            if my_stock not in self.stocks:
                print(my_stock, 'is not in the market')
                continue
            if my_act == 'buy':
                self.buy(my_stock, my_price, my_amount)
            elif my_act == 'sell':
                self.sell(my_stock, my_price, my_amount)
            elif my_act == 'naive': # for trace index
                self.buy(my_stock, my_price, my_amount, True)
            else:
                #TODO
                pass


    def now_epoch(self):
        return self.tot_epochs - self.epoch_offset
    

    #TODO zhang_ting & die_ting not considered
    def buy(self, stock, price, amount, naive = False):
        #for tracing large index not able to buy 100 onetime
        unit = 1
        if not naive:
            amount = amount // 100 * 100
            unit = 100
            
        epoch_idx = find_today_idx(self.today, self.stocks[stock].date, -self.epoch_offset)
        high_price = self.stocks[stock].high_price[epoch_idx]
        low_price = self.stocks[stock].low_price[epoch_idx]
        is_sh = False
        if stock.startswith('sh'):
            is_sh = True
        succ = price >= low_price and amount > 0 #TODO not zhang_ting
        if naive:
            succ = True
        act_item = ('buy', self.now_epoch(), succ, stock, price, amount)
        trans_item = None
        if succ:
            if price >= high_price:
                price = high_price
            fee = buy_fee(amount, price, is_sh)
            #print(amount, fee + price * amount, self.account.money)
            while (fee + price * amount > self.account.money):
                amount -= unit
                fee = buy_fee(amount, price, is_sh)
            if amount <= 0:
                trans_item = ('buy', self.now_epoch(), False, stock, price, 0)
            else:
                self.account.money -= fee + price * amount
                self.account.stocks[stock] += amount
                self.account.stocks_money[stock] += fee + price * amount
                trans_item = ('buy', self.now_epoch(), True, stock, price, amount)
        else:
            trans_item = ('buy', self.now_epoch(), False, stock, price, 0)
        self.profile_data.add_journal(act_item, trans_item)
        
    def sell(self, stock, price, amount):
        epoch_idx = find_today_idx(self.today, self.stocks[stock].date, -self.epoch_offset)
        high_price = self.stocks[stock].high_price[epoch_idx]
        low_price = self.stocks[stock].low_price[epoch_idx]
        succ = price <= high_price and amount > 0 #TODO not die_ting
        act_item = ('sell', self.now_epoch(), succ, stock, price, amount)
        trans_item = None
        if succ:
            if price <= low_price:
                price = low_price
            if amount > self.account.stocks[stock]:
                amount = self.account.stocks[stock]
            fee = sell_fee(amount, price)
            self.account.money += price * amount - fee
            self.account.stocks[stock] -= amount
            self.account.stocks_money[stock] -= price * amount - fee
            if self.account.stocks[stock] == 0:
                self.account.stocks_money[stock] = 0
            trans_item = ('sell', self.now_epoch(), True, stock, price, amount)
        else:
            trans_item = ('sell', self.now_epoch(), False, stock, price, 0)
        self.profile_data.add_journal(act_item, trans_item)


if __name__ == '__main__':
    pass
