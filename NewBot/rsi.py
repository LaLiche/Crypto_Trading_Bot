
import numpy as np
from abstractIndicator import abstractIndicator

class rsi(abstractIndicator):
    def __init__(self):
        super(rsi,self).__init__()
        self.zone = 0 # 0 : pas de zones, 1 : zone 1, 2 : zone 2, 3 : zone 3
        self.priceZ1 = 99999
        self.rsiZ2 = 0
        self.memory = 20
        self.countOpen = 0
        self.countClose = 0
        self.period = 14
        self.currentRSI = 0

    def conditionOpen(self,prices):
        currentRSI = self.computeRSI(prices)
        if self.countOpen > self.memory:
            self.resetOpen()
        if self.zone == 1 :
            self.priceZ1 = mini(prices[-1],self.priceZ1) # on stocke le prix minimal
            if self.currentRSI > 30: #on passe en zone 2
                self.rsiZ2 = self.currenRSI
                self.zone = 2
        elif self.zone == 2:
            self.rsiZ2 = maxi(self.currenRSI,self.rsiZ2) # on stocke le rsi de la zone 2
            if prices[-1] < self.priceZ1: # divergence : on passe en zone 3
                self.zone = 3
        elif self.zone == 3:
            if self.currentRSI > self.rsiZ2: # achat
                self.resetOpen()
                return True
        else:
            if self.currentRSI < 30:
                self.countOpen = 0
                self.zone = 1
        if self.zone != 0:
            self.countOpen += 1
        return False

    def conditionClose(self):
            if self.countClose > memory:
                self.resetClose()
            self.currentRSI = self.computeRSI(prices)
            if self.zone == 1:
                self.priceZ1 = maxi(prices[-1],self.priceZ1) # on stocke le prix maximal
                if self.currentRSI < 70: #on passe en zone 2
                    self.rsiZ2 = self.currentRSI
                    self.zone = 2
            elif self.zone == 2:
                self.rsiZ2 = mini(self.currenRSI,self.rsiZ2) # on stocke le rsi de la zone 2
                if prices[-1] > self.priceZ1: # divergence : on passe en zone 3
                    self.zone = 3
            elif self.zone == 3:
                if self.currentRSI > self.rsiZ2: #on passe en zone 4
                    self.resetClose()
                    return True
            else:
                if self.currentRSI > 70:
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

    def computeRSI(self,prices):
        deltas = np.diff(prices)
        seed = deltas[:self.period+1]
        up = seed[seed >= 0].sum()/self.period
        down = -seed[seed < 0].sum()/self.period
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:self.period] = 100. - 100./(1. + rs)
        for i in range(self.period, len(prices)):
            delta = deltas[i - 1]  # cause the diff is 1 shorter
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(self.period - 1) + upval)/self.period
            down = (down*(self.period - 1) + downval)/self.period
            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)
        if len(prices) > self.period:
            return rsi[-1]
        else:
            return 50 # output a neutral amount until enough prices in list to calculate RSI


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
