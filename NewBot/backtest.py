import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe
from stratRsi import stratRsi

def main(argv):
	chart = BotChart("poloniex","BTC_ETH",86400,'2017-01-01 14:00:00','2017-12-12 20:53:20')

	strategy = stratRsi()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

	graphe = PlotGraphe(chart,strategy)
	graphe.plotChart()

if __name__ == "__main__":
	main(sys.argv[1:])
