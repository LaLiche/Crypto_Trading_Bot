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
