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
		self.indicators = BotIndicators() #

	def tick(self,candlestick):
		self.currentPrice = float(candlestick.close)
		self.prices.append(self.currentPrice)
		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)
		self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving expAverage: "+str(self.indicators.expAverage.average))
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
			if self.indicators.conditionOpen(self.prices,candlestick):
				self.trades.append(BotTrade(self.currentPrice,stopLoss=.0001))

		for trade in openTrades:
			if self.conditionClose(self.prices,candlestick):
				trade.close(self.currentPrice)

	def updateOpenTrades(self,candlestick):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice,candlestick)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
