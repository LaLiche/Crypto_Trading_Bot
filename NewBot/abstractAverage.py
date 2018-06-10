
from abstractIndicator import abstractIndicator

class abstractAverage(object):

    def __init__(self,nbPeriod):
        super(abstractAverage,self).__init__()
        self.average = 0
        self.nbPeriod = nbPeriod

    def conditionOpen(self):
        raise NotImplementedError

    def conditionClose(self):
        raise NotImplementedError
