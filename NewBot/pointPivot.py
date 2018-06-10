
class pointPivot(object):

    def __init__(self):
        self.pivot = 0

    def computePivot(self,candlestick):
        self.pivot = (candlestick.high + candlestick.low + candlestick.close)/float(3)
