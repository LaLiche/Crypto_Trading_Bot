import sys, getopt
import time

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick
from stratRsi2 import stratRsi2

def main(argv):

	pair = "USDT_ETH"
	debut = '2017-08-01 14:00:00'
	fin = '2018-08-01 20:53:20'
	period = 14400

	chart = BotChart("poloniex",pair,period,backtest=False)

	strategy = stratRsi2()

	candlesticks = []
	developingCandlestick = BotCandlestick()

	while True:
		try:
			developingCandlestick.tick(chart.getCurrentPrice())
		except urllib2.URLError:
			time.sleep(int(30))
			developingCandlestick.tick(chart.getCurrentPrice())

		if (developingCandlestick.isClosed()):
			candlesticks.append(developingCandlestick)
			strategy.tick(developingCandlestick)
			developingCandlestick = BotCandlestick()

		time.sleep(int(30))

if __name__ == "__main__":
	main(sys.argv[1:])
