import numpy as np
import matplotlib.pyplot as plt
import uuid
#import pandas as pd
#import math
#import csv

class Asset:
    """ Asset(s) that can be bought and sold by the traders. The asset will be able to be generated, evolved, and traded."""

    def __init__(self, true_price=100, trading_price=100, ma_short=10, ma_long=50, period_growth=0.2, history_length=100):
        """Initalise asset with 200 periods of trading history (generated randomly) and with starting price as 100."""
        self.id = uuid.uuid4()
        self.true_price = true_price
        self.trading_price = trading_price
        self.period_growth = period_growth
        self.history_length = history_length
        self.history_true = Asset.history(self, traded=False)
        self.history_traded = Asset.history(self, traded=True)
        if ma_short:
            self.ma_short = Asset.ma_history(self, self.history_traded, ma_short)
        if ma_long:
            self.ma_long = Asset.ma_history(self, self.history_traded, ma_long)


    def history(self, end_price=100, traded=True):
        """Return a randomly generated 1D numpy array ending in the desired end price with the desired length."""
        history = list([end_price])
        for s in range(self.history_length - 1):
            if traded:
                history.append(history[-1] + np.random.normal(-0.1, 1, None))
            else:
                history.append(history[-1] - self.period_growth + np.random.normal(0, 0.1, None))
        history.reverse()
        return np.array(history)

    def update_true(self):
        self.true_price = self.history_true[-1] + self.period_growth +np.random.normal(0, np.random.uniform(), None)
        np.append(self.history_true, self.true_price)

    def update_traded(self, trading_price):
        self.trading_price = trading_price
        np.append(self.history_traded, self.traded_price)

    def ma_history(self, x, w):
        ma = np.convolve(x, np.ones(w), 'valid') / w
        addition = x[:w-1]
        total = np.append(addition, ma)
        return total

    def update_ma(self, x, w):
        """ Takes """

class Trader:
    """A base class from which traders can be designed. Contains the basic framework from which trader subclasses of unique strategies can be generated.
    Each subclass of traders has its own strategies that are used to determine trading decisions in any given period."""

    def __init__(self, id, money, stock):
        self.id = id
        self.money = money
        self.stock = stock
        self.account = self.money + self.stock*100 #Starting trading price is 100
        self.a = np.random.normal(0.44, 0.05, None) #alpha, beta and gamma values for prospect theory functions, some slight variation across traders
        self.b = np.random.normal(0.49, 0.05, None)
        self.l = np.random.uniform(1.03, 1.06, None)

    def place_bid(self, bid_price, quantity):
        return (quantity, bid_price, self.id, True)

    def place_ask(self, ask_price, quantity):
        return (quantity, ask_price, self.id, False)

    def value(self, x):
        self.x = x
        self.a = 0.44
        self.b = 0.49
        self.l = 1.06
        if self.x >= 0:
            self.val = self.x**self.a
        elif self.x < 0:
            self.val = -self.l*(-self.x)**self.b
        return self.val

    def weighting(self, x):
        return x

class Arbitrageur(Trader):
    """Type of trader who relies on the true price to make trading decisions."""

class Chartist(Trader):
    """Type of trader who relies on past prices and various statistical indicators to make trading decisions."""

class ValueTrader(Trader):
    """Type of trader who drip feeds the asset into a portfolio, believes in long term growth, not short term returns."""

class NoiseTrader(Trader):
    """Type of trader who has no set strategy - buys and sells randomly to provide volume in the market."""

print("Hello!")
a1 = Asset(1)
a1_10ma = a1.ma_history(a1.history_traded, 10)
print("Length of trading history: ", a1.history_traded.size)
print("Length of true history: ", a1.history_true.size)
print(a1_10ma.size)

plt.plot(a1.history_traded)
plt.plot(a1.history_true)
plt.plot(a1_10ma)
plt.show()