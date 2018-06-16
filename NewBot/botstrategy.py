from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.trades = []
		self.low = []
		self.high = []
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 1
		self.indicators = BotIndicators()

	def tick(self,candlestick):
		self.currentPrice = float(candlestick.close)
		self.prices.append(self.currentPrice)
		self.low.append(candlestick.low)
		self.high.append(candlestick.high)
		self.evaluatePositions(candlestick)
		self.updateOpenTrades(candlestick)
		self.showPositions()

	def evaluatePositions(self,candlestick):
		# on ne gere que un seul trade
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)
		if (len(openTrades) < self.numSimulTrades):
			if self.conditionOpen(candlestick):
				self.trades.append(BotTrade(self.currentPrice,candlestick.startTime,stopLoss=.0001))

		for trade in openTrades:
			if self.conditionClose(trade):
				trade.close(self.currentPrice,candlestick.startTime + candlestick.period)

	def updateOpenTrades(self,candlestick):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice,candlestick)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()

	def conditionOpen(self,candlestick):
		raise NotImplementedError

	def conditionClose(self,trade):
		raise NotImplementedError
