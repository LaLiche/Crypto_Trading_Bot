from poloniex import poloniex
import urllib, json
import pprint
from botcandlestick import BotCandlestick
import time
import timetranslate as tt

class BotChart(object):
	def __init__(self, exchange, pair, period, startTime=False, endTime=False, backtest=True):
		self.pair = pair
		self.period = period
		if backtest:
			self.startTime = tt.TimetoFloat(startTime)
			self.endTime = tt.TimetoFloat(endTime)
		self.compteur = 0
		self.data = []

		if (exchange == "poloniex"):
			self.conn = poloniex('key goes here','Secret goes here')

			if backtest:
				poloData = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
				for datum in poloData:
					if (datum['open'] and datum['close'] and datum['high'] and datum['low']):
						self.data.append(BotCandlestick(self.period,datum['open'],datum['close'],datum['high'],datum['low'],self.startTime+self.compteur*self.period,datum['weightedAverage']))
						self.compteur += 1

		if (exchange == "bittrex"):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+str(self.period)+"&_="+str(self.startTime)
				response = urllib.urlopen(url)
				rawdata = json.loads(response.read())

				self.data = rawdata["result"]

	def getPoints(self):
		return self.data

	def getCurrentPrice(self):
		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice

	def getSigma(self):
		volatilite = []
		for c in self.data:
			volatilite.append((c.high-c.low)/c.low*100)
		m = sum(volatilite,0.0)/len(volatilite)
		v = sum([(x-m)**2 for x in volatilite],0.0)/len(volatilite)
		s = v ** 0.5
		return s
