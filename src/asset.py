import numpy as np
import matplotlib.pyplot as plt
import uuid
#import math
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
                history.append(history[-1] + np.random.normal(-self.period_growth, 1, None))
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
        """Return a numpy array of moving averages of the supplied array. For the intial values where there is an incomplete window, the values of the supplied array are used."""
        ma = np.convolve(x, np.ones(w), 'valid') / w
        addition = x[:w-1]
        total = np.append(addition, ma)
        return total

    def update_ma(self, x, ma, w):
        """Updates an array of moving averages with the final value (to be updated each period)."""
        new_val = np.sum(x[-w:]) / w
        new_ma = np.append(ma, new_val)
        return new_ma

def sigmoid(x): #Used to transform inputs in range (-inf,inf) to (0,1) for probabilities
    return 1/(1 + np.exp(-x))

print("Hello!")
a1 = Asset(ma_short=15, ma_long=50, history_length=200)
print(a1.id)

plt.plot(a1.history_traded, label="Trading Price")
plt.plot(a1.history_true, label="True Price")
plt.plot(a1.ma_short, label="15 Period MA")
plt.plot(a1.ma_long, label="50 Period MA")
plt.legend()
plt.show()