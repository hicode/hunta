#! /usr/bin/env python3


def gerou_sign(stockidx, account, hist, threshold = 0.1):
    avg_price = account.stocks_money[stockidx] / account.stocks[stockidx]
    if hist.close_price[-1] / avg_price < 1.0 - threshold:
        #print('gerou', avg_price, hist.close_price[-1])
        return True
    return False

def luodaiweian_sign(stockidx, account, hist, threshold = 0.2):
    avg_price = account.stocks_money[stockidx] / account.stocks[stockidx]
    if hist.close_price[-1] / avg_price > 1.0 + threshold:
        #print('gerou', avg_price, hist.close_price[-1])
        return True
    return False