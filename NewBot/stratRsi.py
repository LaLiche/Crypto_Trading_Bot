

import numpy as np
from abstractIndicator import abstractIndicator
from botstrategy import BotStrategy

class stratRsi(BotStrategy):
    def __init__(self):
        super(stratRsi,self).__init__()
        self.zone = 0 # 0 : pas de zones, 1 : zone 1, 2 : zone 2, 3 : zone 3
        self.priceZ1 = 99999
        self.rsiZ2 = 0
        self.memory = 20
        self.countOpen = 0
        self.countClose = 0

    def condRsiOpen(self):
        rsi = self.indicators.RSI(self.prices)
        if self.countOpen > self.memory:
            self.resetOpen()
        if self.zone == 1 :
            self.priceZ1 = mini(self.prices[-1],self.priceZ1) # on stocke le prix minimal
            if rsi > 30: #on passe en zone 2
                self.rsiZ2 = rsi
                self.zone = 2
        elif self.zone == 2:
            self.rsiZ2 = maxi(rsi,self.rsiZ2) # on stocke le rsi de la zone 2
            if self.prices[-1] < self.priceZ1: # divergence : on passe en zone 3
                self.zone = 3
        elif self.zone == 3:
            if rsi > self.rsiZ2: # achat
                self.resetOpen()
                return True
        else:
            if rsi < 30:
                self.countOpen = 0
                self.zone = 1
        if self.zone != 0:
            self.countOpen += 1
        return False

    def condRsiClose(self):
        rsi = self.indicators.RSI(self.prices)
        if self.countClose > self.memory:
            self.resetClose()
        if self.zone == 1:
            self.priceZ1 = maxi(self.prices[-1],self.priceZ1) # on stocke le prix maximal
            if rsi < 70: #on passe en zone 2
                self.rsiZ2 = rsi
                self.zone = 2
        elif self.zone == 2:
            self.rsiZ2 = mini(self.currenRSI,self.rsiZ2) # on stocke le rsi de la zone 2
            if self.prices[-1] > self.priceZ1: # divergence : on passe en zone 3
                self.zone = 3
        elif self.zone == 3:
            if rsi > self.rsiZ2: #on passe en zone 4
                self.resetClose()
                return True
        else:
            if rsi > 70:
                self.countClose = 0
                self.zone = 1
        if self.zone != 0:
            self.countClose += 1
        return False

    def resetOpen(self):
        self.countOpen = 0
        self.countClose = 0
        self.zone = 0
        self.rsiZ2 = 0
        self.priceZ1 = 999999


    def resetClose(self):
        self.countOpen = 0
        self.countClose = 0
        self.zone = 0
        self.rsiZ2 = 100
        self.priceZ1 = 0

    def conditionOpen(self,candlestick):
        if candlestick.close > self.indicators.computeExpAverage(self.prices,candlestick,10) and candlestick.close > self.indicators.pointPivot(candlestick):
            if self.condRsiOpen():
                return True
        return False

    def conditionClose(self,candlestick):
        if candlestick.close < self.indicators.computeExpAverage(self.prices,candlestick,10) and candlestick.close < self.indicators.pointPivot(candlestick):
            if self.condRsiClose():
				return True
        return False

def maxi(a,b):
    if a > b :
        return a
    else:
        return b

def mini(a,b):
    if a < b :
        return a
    else:
        return b
