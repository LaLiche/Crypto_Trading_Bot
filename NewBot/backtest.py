import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe
from stratRsi import stratRsi
from stratStochastique import stratStochastique

def main(argv):
	trading_chart = BotChart("poloniex","BTC_XMR",300, '2017-06-01 14:00:00','2017-06-07 20:53:20')
	chart_m5 = BotChart("poloniex","BTC_XMR",300,'2017-06-01 14:00:00','2017-06-07 20:53:20')
	chart_m15 = BotChart("poloniex","BTC_XMR",900,'2017-06-01 14:00:00','2017-06-07 20:53:20')
	chart_d1 = BotChart("poloniex","BTC_XMR",86400,'2017-06-01 14:00:00','2017-06-07 20:53:20')
	strategy = stratStochastique(chart_m5,chart_m15,chart_d1)

	# on va stocker les bougies de period 5mn, 15mn, et 1 jour


	for candlestick in trading_chart.getPoints():
		strategy.tick(candlestick)

	graphe = PlotGraphe(chart,strategy)
	graphe.plotChart()

if __name__ == "__main__":
	main(sys.argv[1:])
