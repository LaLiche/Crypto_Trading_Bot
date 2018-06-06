import plotly
from botchart import BotChart

class PlotGraphe(object):
    def __init__(self,chart):
        self.chart = chart

    def plotchart(self):

        # TODO formater la date + ajouter strategies & indicateurs

        open_data = []
        close_data = []
        high_data = []
        low_data = []
        x_data = []

        for c in self.chart.data:
            open_data.append(c.open)
            close_data.append(c.close)
            high_data.append(c.high)
            low_data.append(c.low)
            x_data.append(c.startTime)

        trace = plotly.graph_objs.Candlestick(
            x = x_data,
            open = open_data,
            close = close_data,
            high = high_data,
            low = low_data)

        data = [trace]
        plotly.offline.plot(data,filename='test_graphe.html')
