import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe

def main(argv):
	chart = BotChart("poloniex","BTC_XMR",300)

	strategy = BotStrategy()

	# for candlestick in chart.getPoints():  Uncomment pour test la strategie
		# strategy.tick(candlestick)

	graphe = PlotGraphe(chart)
	graphe.plotchart()

if __name__ == "__main__":
	main(sys.argv[1:])
