import numpy

class BotIndicators(object):
	def __init__(self):
		self.expAverage = 0
		pass

	def momentum(self, dataPoints, period=14):
		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def EMA(self, prices, period):
		x = numpy.asarray(prices)
		weights = None
		weights = numpy.exp(numpy.linspace(-1., 0., period))
		weights /= weights.sum()

		a = numpy.convolve(x, weights, mode='full')[:len(x)]
		a[:period] = a[period]
		return a

	def MACD(self, prices, nslow=26, nfast=12):
		emaslow = self.EMA(prices, nslow)
		emafast = self.EMA(prices, nfast)
		return emaslow, emafast, emafast - emaslow

	def RSI(self, prices, period=14):
		deltas = numpy.diff(prices)
		seed = deltas[:period+1]
		up = seed[seed >= 0].sum()/period
		down = -seed[seed < 0].sum()/period
		if down != 0:
			rs = up/down
		else:
			rs = 1
		rsi = numpy.zeros_like(prices)
		rsi[:period] = 100. - 100./(1. + rs)
		for i in range(period, len(prices)):
 			delta = deltas[i - 1]  # cause the diff is 1 shorter
  			if delta > 0:
 				upval = delta
 				downval = 0.
 			else:
 				upval = 0.
 				downval = -delta

 			up = (up*(period - 1) + upval)/period
 			down = (down*(period - 1) + downval)/period
  			rs = up/down
 			rsi[i] = 100. - 100./(1. + rs)
  		if len(prices) > period:
 			return rsi[-1]
 		else:
 			return 50 # output a neutral amount until enough prices in list to calculate RSI

	def computeExpAverage(self,prices,candlestick,nbPeriod):
		if self.expAverage != 0:
			self.expAverage = (2/float(nbPeriod+1))*candlestick.close+(1-2/float(nbPeriod+1))*self.expAverage
		else:
			self.expAverage = candlestick.close
		return self.expAverage

	def simpleAverage(self,prices,nbPeriod):
	 	return sum(prices[-nbPeriod:]) / float(len(prices[-nbPeriod:]))

	def pointPivot(self,candlestick):
		return (candlestick.high + candlestick.low + candlestick.close)/float(3)

	def bollinger(self,prices,nbPeriod):
		movingAverage = self.simpleAverage(prices,nbPeriod)
		sigma = 0
		for k in range(1,nbPeriod+1):
			sum += (prices[-k] - movingAverage)**2
		sigma = numpy.sqrt(sigma/float(n))
		return [movingAverage - 2*sigma,movingAverage,movingAverage + 2*sigma]
