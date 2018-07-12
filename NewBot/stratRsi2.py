from botstrategy import BotStrategy

class stratRsi2(BotStrategy):
    def __init__(self):
        super(stratRsi2,self).__init__()
        self.derivee = 0
        self.RSI_data = []
        self.RSI_moyenne = []
        self.lastAverage = 0.

    def conditionOpen(self):
        res = False
        self.RSI_data.append(self.indicators.RSI(self.prices,14))
        self.RSI_moyenne.append(self.indicators.expMoyenne(self.RSI_data,12,self.lastAverage))
        # self.RSI_moyenne.append(self.indicators.simpleAverage(self.RSI_data,10))
        self.lastAverage = self.RSI_moyenne[-1]
        if len(self.RSI_moyenne) == 1:
            deriv = 0
        else:
            deriv = (self.RSI_moyenne[-1]-self.RSI_moyenne[-2])
        if self.derivee <=0 and deriv>0. and len(self.RSI_moyenne) > 14:
        # if self.lastAverage <= self.RSI_moyenne[-1] and len(self.RSI_moyenne) > 14:
            # print deriv
            res = True
        self.derivee = deriv
        return res


    def conditionClose(self,trade):
        res = False
        self.RSI_data.append(self.indicators.RSI(self.prices,14))
        self.RSI_moyenne.append(self.indicators.expMoyenne(self.RSI_data,12,self.lastAverage))
        # self.RSI_moyenne.append(self.indicators.simpleAverage(self.RSI_data,7))
        self.lastAverage = self.RSI_moyenne[-1]
        if len(self.RSI_moyenne) == 1:
            deriv = 0
        else:
            deriv = (self.RSI_moyenne[-1]-self.RSI_moyenne[-2])
        if self.derivee >=0 and deriv<-0. and len(self.RSI_moyenne) > 14:
        # if self.lastAverage >= self.RSI_moyenne[-1] and len(self.RSI_moyenne) > 14:
            res = True
        self.derivee = deriv
        return res
