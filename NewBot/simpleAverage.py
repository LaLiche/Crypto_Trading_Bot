
from abstractAverage import abstractAverage

class simpleAverage(abstractAverage):

    def __init__(self,nbPeriod):
        super(simpleAverage,self).__init__(nbPeriod)

    def computeAverage(self):
		self.average = sum(self.prices[-nbPeriod:]) / float(len(self.prices[-nbPeriod:]))
