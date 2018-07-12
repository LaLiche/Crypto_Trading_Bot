import numpy as np
from botstrategy import BotStrategy

# strategie en periode de 1 mn qui utilisent des indicateurs d'autres unite de temps pour detecter un sens prioritaire
class stratStochastique(BotStrategy):
    def __init__(self, chart_m5, chart_m15, chart_d1):
        super(stratStochastique,self).__init__()
        self.stopLoss = 0.001
        self.data_m5 = init_chart(chart_m5)
        self.data_m15 = init_chart(chart_m15)
        self.data_d1 = init_chart(chart_d1)
        self.inf_20 = False
        self.moyenne_timming = [0,0,0,0]
        self.moyenne_m5 = [0,0,0,0]
        self.moyenne_m15 = [0,0,0,0]

    def sensPrioAchat(self,candlestick):
        p = self.currentPrice
        self.moyenne_timming[0] = self.indicators.expAverage(self.prices,candlestick,100,self.moyenne_timming[0])
        self.moyenne_timming[1] = self.indicators.expAverage(self.prices,candlestick,300,self.moyenne_timming[1])
        self.moyenne_timming[2] = self.indicators.expAverage(self.prices,candlestick,600,self.moyenne_timming[2])
        self.moyenne_timming[3] = self.indicators.expAverage(self.prices,candlestick,1000,self.moyenne_timming[3])
        sens_m1 = p > self.moyenne_timming[0] and p > self.moyenne_timming[1] and p > self.moyenne_timming[2] and p > self.moyenne_timming[3]
        self.moyenne_m5[0] = self.indicators.expAverage(self.data_m5[0],candlestick,100,self.moyenne_m5[0])
        self.moyenne_m5[1] = self.indicators.expAverage(self.data_m5[0],candlestick,300,self.moyenne_m5[1])
        self.moyenne_m5[2] = self.indicators.expAverage(self.data_m5[0],candlestick,600,self.moyenne_m5[2])
        self.moyenne_m5[3] = self.indicators.expAverage(self.data_m5[0],candlestick,1000,self.moyenne_m5[3])
        sens_m5 = p > self.moyenne_m5[0] and p > self.moyenne_m5[1] and p > self.moyenne_m5[2] and p > self.moyenne_m5[3]
        self.moyenne_m15[0] = self.indicators.expAverage(self.data_m15[0],candlestick,100,self.moyenne_m15[0])
        self.moyenne_m15[1] = self.indicators.expAverage(self.data_m15[0],candlestick,300,self.moyenne_m15[1])
        self.moyenne_m15[2] = self.indicators.expAverage(self.data_m15[0],candlestick,600,self.moyenne_m15[2])
        self.moyenne_m15[3] = self.indicators.expAverage(self.data_m15[0],candlestick,1000,self.moyenne_m15[3])
        sens_m15 = p > self.moyenne_m15[0] and p > self.moyenne_m15[1] and p > self.moyenne_m15[2] and p > self.moyenne_m15[3]
        pivot_d1 = (self.data_d1[0][-1] + self.data_d1[1][-1] + self.data_d1[2][-1])/float(3)
        sens_pivot = p > pivot_d1
        return sens_m1 and sens_m5 and sens_m15 and sens_pivot

    def condStochastique(self,candlestick):
        stochastique = self.indicators.stochastique(self.prices,self.low,self.high,14)
        if (stochastique < 20):
            self.inf_20 = True
            return False
        else:
            if(self.inf_20):
                self.inf_20 = False
                if self.sensPrioAchat(candlestick):
                    print(stochastique)
                return True
            else:
                self.inf_20 = False
                return False

    def conditionOpen(self,candlestick):
        # necessaire que condStochastique soit appelee dans cette methode
        st = self.condStochastique(candlestick)
        prio = self.sensPrioAchat(candlestick)
        print("dans conditionOpen")
        if prio:
            print("et prio est vrai")
        return prio and st

    def conditionClose(self,candlestick,trade):
        return self.currentPrice - trade.entryPrice > self.stopLoss

def init_chart(chart):
    prices = [] # close
    high = []
    low = []
    for candlestick in chart.getPoints():
        prices.append(candlestick.close)
        high.append(candlestick.high)
        low.append(candlestick.low)
    return [prices,low,high];
