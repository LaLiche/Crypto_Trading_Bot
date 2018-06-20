import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe
from stratRsi import stratRsi
from stratSaitta import stratSaitta
from stratStochastique import stratStochastique

def main(argv):
	# chart = BotChart("poloniex","BTC_ETH",1800,'2018-01-01 14:00:00','2018-03-12 20:53:20')


	# on va stocker les bougies de period 5mn, 15mn, et 1 jour
	pair = "BTC_XMR"
	debut = '2017-06-01 14:00:00'
	fin = '2017-08-01 20:53:20'
	chart = BotChart("poloniex",pair,300,debut,fin)
	chart_m5 = BotChart("poloniex",pair,900,debut,fin)
	chart_m15 = BotChart("poloniex",pair,1800,debut,fin)
	chart_d1 = BotChart("poloniex",pair,86400,debut,fin)
	strategy = stratStochastique(chart_m5,chart_m15,chart_d1)

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
