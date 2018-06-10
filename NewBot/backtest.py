import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe

def main(argv):
	chart = BotChart("poloniex","BTC_XMR",300,'2017-04-01 14:00:00','2017-04-07 20:53:20')

	strategy = BotStrategy()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

	graphe = PlotGraphe(chart,strategy)
	graphe.plotChart()

if __name__ == "__main__":
	main(sys.argv[1:])
