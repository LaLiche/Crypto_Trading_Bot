import numpy
from rsi import rsi
from expAverage import expAverage
from pointPivot import pointPivot

class BotIndicators(object):
	def __init__(self):
		self.rsi = rsi()
		self.expAverage = expAverage(10)
		self.pointPivot = pointPivot()

	def conditionOpen(self, prices, candlestick):
		self.expAverage.computeAverage(prices,candlestick)
		if candlestick.close > self.expAverage.average and candlestick.close > self.pointPivot.pivot:
			if self.rsi.conditionOpen(prices):
				return True
		return False

	def conditionClose(self, prices, candlestick):
		if candlestick.close < expAverage.average and candlestick.close < pointPivot.pivot:
			if rsi.conditionClose(prices):
				return True
		return False

	def momentum (self, dataPoints, period=14):
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

	def RSI (self, prices, period=14):
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
