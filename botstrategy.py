from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade


class BotStrategy(object):
	def __init__(self,short_mode=False,backtest=True):
		self.capital = 1000
		self.output = BotLog()
		self.prices = []
		self.trades = []
		self.low = []
		self.high = []
		self.currentPrice = ""
		self.numSimulTrades = 100000000 # inutile si seulement signaux !
		self.indicators = BotIndicators()
		# self.stopLoss = 2 * self.indicators.average_true_range(self.high,self.low,self.prices)
		self.stopLoss = 0 # inutile pour signaux

		self.short_mode = short_mode
		self.backtest = backtest

	def tick(self,candlestick):
		self.currentPrice = float(candlestick.close)
		self.prices.append(self.currentPrice)
		self.low.append(candlestick.low)
		self.high.append(candlestick.high)
		# self.stopLoss = 2 * self.indicators.average_true_range(self.high,self.low,self.prices)
		self.evaluatePositions(candlestick)
		self.updateOpenTrades(candlestick)
		# self.showPositions()

	def evaluatePositions(self,candlestick):
		# on ne gere que un seul trade
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)
		if (len(openTrades) < self.numSimulTrades):
			if self.conditionOpen():
				self.trades.append(BotTrade(self.currentPrice,candlestick.startTime,self.stopLoss))
				try:
					if self.backtest == False:
						if self.short_mode:
							self.output.sendNotif("SELL","Signal Short | Price: "+str(self.currentPrice) + ' | Period: ' +str(self.period))
						else:
							self.output.sendNotif("BUY","Signal Long | Price: "+str(self.currentPrice) + ' | Period: ' +str(self.period))
				except Exception as e:
					print e
		for trade in openTrades:
			if self.conditionClose(trade):
				print("vendu par target: "+str(self.currentPrice))
				trade.close(self.currentPrice,candlestick.startTime)

	def updateOpenTrades(self,candlestick):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice,candlestick)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()

	def conditionOpen(self):
		raise NotImplementedError

	def conditionClose(self,trade):
		raise NotImplementedError
