import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe
from stratRsi import stratRsi
from stratSaitta import stratSaitta

def main(argv):
	chart = BotChart("poloniex","BTC_LTC",1800,'2017-01-01 14:00:00','2017-02-12 20:53:20')

	strategy = stratSaitta()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

	graphe = PlotGraphe(chart,strategy)
	graphe.plotChart()

if __name__ == "__main__":
	main(sys.argv[1:])
