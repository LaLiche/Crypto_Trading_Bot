import numpy as np
from botstrategy import BotStrategy

class stratRsi(BotStrategy):
    def __init__(self):
        super(stratRsi,self).__init__()
        self.zone = 0 # 0 : pas de zones, 1 : zone 1, 2 : zone 2, 3 : zone 3
        self.priceZ1 = 9999999999
        self.rsiZ1 = 100
        self.rsiZ2 = 0
        self.rsiZ3 = 100
        self.memory = 1000
        self.countOpen = 0
        self.countClose = 0
        self.distanceMin = 5
        # self.stopLoss = 2 * self.indicators.average_true_range(self.high,self.low,self.prices)
        # self.stopLoss = 1000

        self.derivee = 0


    def condRsiOpen(self):
        rsi = self.indicators.RSI(self.prices)

        if self.countOpen > self.memory:
            self.resetOpen()


        if self.zone == 1:
            self.rsiZ1 = min(rsi,self.rsiZ1)
            self.priceZ1 = min(self.currentPrice,self.priceZ1) # on stocke le prix minimal
            if rsi > 30: #on passe en zone 2
                self.rsiZ2 = rsi
                self.zone = 2


        elif self.zone == 2:
            self.rsiZ2 = max(rsi,self.rsiZ2) # on stocke le rsi de la zone 2
            if self.currentPrice < self.priceZ1*0.98 :
                if rsi < self.rsiZ2-(self.rsiZ1-self.rsiZ2)/3 and rsi > self.rsiZ1 and self.countOpen >= self.distanceMin: # divergence : on passe en zone 3
                    self.zone = 3
                elif rsi < self.rsiZ1:
                    self.rsiZ1 = rsi
                    self.zone = 1
            if rsi > 70: # on reset si le rsi remonte trop
                self.resetOpen()


        elif self.zone == 3:
            self.rsiZ3 = min(rsi,self.rsiZ3)
            if rsi > self.rsiZ2: # achat
                self.resetOpen()
                return True
            elif self.rsiZ3 < self.rsiZ1:
                # self.resetOpen()
                self.rsiZ1 = rsi
                self.priceZ1 = self.currentPrice
                self.zone = 1
                self.countOpen = 0



        else:
            if rsi < 30:
                self.resetOpen()
                self.zone = 1

        if self.zone != 0:
            self.countOpen += 1
        return False



    def condRsiClose(self):
        rsi = self.indicators.RSI(self.prices)
        if self.countClose > self.memory:
            self.resetClose()


        if self.zone == 1:
            self.rsiZ1 = max(rsi,self.rsiZ1)
            self.priceZ1 = max(self.currentPrice,self.priceZ1) # on stocke le prix maximal
            if rsi < 70: #on passe en zone 2
                self.rsiZ2 = rsi
                self.zone = 2


        elif self.zone == 2:
            self.rsiZ2 = min(rsi,self.rsiZ2) # on stocke le rsi de la zone 2
            if self.currentPrice > self.priceZ1*1.02:
                if rsi > self.rsiZ1-(self.rsiZ1-self.rsiZ2)/3 and rsi < self.rsiZ1 and self.countClose >= self.distanceMin:
                    self.zone = 3
                elif rsi > self.rsiZ1:
                    self.rsiZ1 = rsi
                    self.zone = 1
            if rsi < 30: # on reset si le rsi descend trop
                self.resetClose()


        elif self.zone == 3:
            self.rsiZ3 = max(rsi,self.rsiZ3)
            if rsi < self.rsiZ2: #on passe en zone 4
                self.resetClose()
                return True
            elif self.rsiZ3 > self.rsiZ1:
                self.rsiZ1 = rsi
                self.zone = 1
                self.countClose = 0
                self.priceZ1 = self.currentPrice


        else:
            if rsi > 70:
                self.resetClose()
                self.zone = 1

        if self.zone != 0:
            self.countClose += 1
        return False



    def conditionRsi2Open(self):
        return 30 > self.indicators.RSI(self.prices)


    def conditionRsi2Close(self):
        return 70 < self.indicators.RSI(self.prices)


    def condBreakoutClose(self):
        resistance = self.indicators.saitta_support_resistance(self.high,self.low,12)[1]
        return self.currentPrice > resistance


    def resetOpen(self):
        self.countOpen = 0
        self.countClose = 0
        self.zone = 0
        self.rsiZ2 = 0
        self.priceZ1 = 999999
        self.rsiZ1 = 100
        self.rsiZ3 = 100

    def resetClose(self):
        self.countOpen = 0
        self.countClose = 0
        self.zone = 0
        self.rsiZ2 = 100
        self.priceZ1 = 0
        self.rsiZ1 = 0
        self.rsiZ3 = 0

    def conditionOpen(self,candlestick):
        if len(self.prices) > 14:
            return self.condRsiOpen()
        else:
            return False

    def conditionClose(self,candlestick,trade):
        return self.conditionRsi2Close()


    # def conditionOpen(self,candlestick):
    #     span_B = self.indicators.simpleAverage(self.prices,200)
    #     if self.prices[-1] > span_B:
    #         return self.conditionRsi2Open()
    #     # return (self.condRsiOpen() or self.conditionRsi2Open())
    #     else:
    #         return self.condRsiOpen()
    #
    # def conditionClose(self,candlestick,trade):
    #     span_B = self.indicators.simpleAverage(self.prices,200)
    #     if self.prices[-1] > span_B:
    #         return self.condRsiClose()
    #     # return (self.condRsiClose() or self.conditionRsi2Close())
    #     else:
    #         return self.conditionRsi2Close()
