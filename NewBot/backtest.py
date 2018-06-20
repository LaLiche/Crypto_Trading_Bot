import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe
from stratRsi import stratRsi
from stratSaitta import stratSaitta

def main(argv):
	chart = BotChart("poloniex","BTC_ETH",1800,'2018-01-01 14:00:00','2018-01-12 20:53:20')

	strategy = stratRsi()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

	graphe = PlotGraphe(chart,strategy)
	graphe.plotChart()

	sigma = chart.getSigma()*float(chart.compteur)**0.5
	perf = graphe.perf
	sharpeRatio = perf/sigma
	print("\n Ratio de Sharpe: "+str(sharpeRatio)+"\n")

if __name__ == "__main__":
	main(sys.argv[1:])
