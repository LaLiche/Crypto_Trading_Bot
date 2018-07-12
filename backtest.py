import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from plotgraphe import PlotGraphe
from stratRsi import stratRsi
from stratRsi2 import stratRsi2
from stratSaitta import stratSaitta
from stratStochastique import stratStochastique

def main(argv):
	# chart = BotChart("poloniex","BTC_ETH",1800,'2018-01-01 14:00:00','2018-03-12 20:53:20')

	pair = "USDT_ETH"
	debut = '2016-11-02 14:00:00'
	fin = '2018-08-14 20:53:20'
	period = 14400

	chart = BotChart("poloniex",pair,period,debut,fin)


	# on va stocker les bougies de period 5mn, 15mn, et 1 jour
	# chart_m5 = BotChart("poloniex",pair,900,debut,fin)
	# chart_m15 = BotChart("poloniex",pair,1800,debut,fin)
	# chart_d1 = BotChart("poloniex",pair,86400,debut,fin)
	# strategy = stratStochastique(chart_m5,chart_m15,chart_d1)

	strategy = stratRsi(period)
	# strategy = stratRsi2()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

	graphe = PlotGraphe(chart,strategy)
	graphe.plotChart()

	try:
		sigma = chart.getSigma()*float(chart.compteur)**0.5
		perf = graphe.perf
		sharpeRatio = perf/sigma
		print("\n Perforance: "+str(perf))
		print("\n Ratio de Sharpe: "+str(sharpeRatio)+"\n")
	except Exception as e:
		pass


if __name__ == "__main__":
	main(sys.argv[1:])
