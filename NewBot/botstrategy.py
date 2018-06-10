from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 1
		self.indicators = BotIndicators()

	def tick(self,candlestick):
		self.currentPrice = float(candlestick.priceAverage)
		self.prices.append(self.currentPrice)

		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)

		self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions(candlestick)
		self.updateOpenTrades(candlestick)
		self.showPositions()

	def evaluatePositions(self,candlestick):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
				self.trades.append(BotTrade(self.currentPrice,candlestick.startTime,stopLoss=.0001))

		for trade in openTrades:
			if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
				trade.close(self.currentPrice,candlestick.startTime)

	def updateOpenTrades(self,candlestick):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice,candlestick)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
