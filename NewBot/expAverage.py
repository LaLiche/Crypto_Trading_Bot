
from abstractAverage import abstractAverage

class expAverage(abstractAverage):

    def __init__(self,nbPeriod):
        super(expAverage,self).__init__(nbPeriod)

    def computeAverage(self,prices,candlestick):
        if self.average != 0:
            self.average = (2/float(self.nbPeriod+1))*candlestick.close+(1-2/float(self.nbPeriod+1))*self.average
        else:
            self.average = candlestick.close
