from botstrategy import BotStrategy

class stratSaitta(BotStrategy):
    def __init__(self):
        super(stratSaitta,self).__init__()

    def conditionOpen(self,candlestick):
        resistance = self.indicators.saitta_support_resistance(self.high,self.low,12)[1]
        return self.currentPrice > resistance

    def conditionClose(self,candlestick):
        support = self.indicators.saitta_support_resistance(self.high,self.low,12)[0]
        return self.currentPrice < support
