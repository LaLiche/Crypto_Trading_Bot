import plotly
from botchart import BotChart
from poloniex import poloniex


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

        layout = {
            'title': self.chart.pair+" "+str(self.chart.period)+" s",
            'yaxis': {'title': self.chart.pair},
            'shapes': [{
                'x0': '2016-12-09', 'x1': '2016-12-09',
                'y0': 0, 'y1': 1, 'xref': 'x', 'yref': 'paper',
                'line': {'color': 'rgb(30,30,30)', 'width': 1}
            }]
            }

        data = [trace]
        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig,filename='test_graphe.html')
