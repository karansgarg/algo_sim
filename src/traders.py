import numpy as np
import uuid
#import matplotlib.pyplot as plt
#import pandas as pd
#import math
#import csv

class Trader:
    """A base class from which traders can be designed. Contains the basic framework from which trader subclasses of unique strategies can be generated.
    Each subclass of traders has its own strategies that are used to determine trading decisions in any given period."""

    def __init__(self, money, stock):
        self.id = uuid.uuid4()
        self.money = money
        self.stock = stock
        self.account = self.money + self.stock*100 #Starting trading price is 100
        self.a = np.random.normal(0.44, 0.05, None) #alpha, beta, lambda and gamma values for prospect theory functions, some slight variation across traders
        self.b = np.random.normal(0.49, 0.05, None)
        self.l = np.random.uniform(1.03, 1.06, None)
        self.g = np.random.uniform(0.4, 0.6, None)
        self.active = np.random.uniform(0.2, 1, None) #Rate of trading activity in the market, i.e. how often they enter the market
        self.faith = np.random.uniform() #The proclivity of the agent to stick to its current strategy


    def place_bid(self, bid_price, quantity):
        return (quantity, bid_price, self.id, True)

    def place_ask(self, ask_price, quantity):
        return (quantity, ask_price, self.id, False)

    def value(self, x):
        if x >= 0:
            self.val = x**self.a
        elif x < 0:
            self.val = -self.l*(-x)**self.b
        return self.val

    def weighting(self, p):
        return (p**self.g)/((p**self.g+(1-p)**self.g)**(1/self.g))

class Arbitrageur(Trader):
    """Type of trader who relies on the true price to make trading decisions."""

class Chartist(Trader):
    """Type of trader who relies on past prices and various statistical indicators to make trading decisions."""

class ValueTrader(Trader):
    """Type of trader who drip feeds the asset into a portfolio, believes in long term growth, not short term returns."""

class NoiseTrader(Trader):
    """Type of trader who has no set strategy - buys and sells randomly to provide volume in the market."""
