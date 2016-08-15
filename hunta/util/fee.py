#! /usr/bin/env python3

from .util import floor_money

def sell_fee(share, price):
    stamp_duty = floor_money(share * price * 0.001)
    transfer_fee = floor_money(0.6 * share / 1000)
    commission_fee = floor_money(share * price * 0.001)
    return stamp_duty + transfer_fee + commission_fee

def buy_fee(share, price, is_shanghai = True):
    transfer_fee = 0
    if is_shanghai:
        transfer_fee = floor_money(0.6 * share / 1000)
    commission_fee = floor_money(share * price * 0.001)
    return transfer_fee + commission_fee

if __name__ == '__main__':
    print('buy', buy_fee(10000, 10))
    print('sell', sell_fee(10000, 10.10))