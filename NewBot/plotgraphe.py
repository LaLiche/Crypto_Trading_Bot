import plotly
from botchart import BotChart
from poloniex import poloniex
import timetranslate as tt


class PlotGraphe(object):
    def __init__(self,chart):
        self.chart = chart

    def plotchart(self):

        # TODO formater la date + ajouter strategies & indicateurs

        open_data = []
        close_data = []
        high_data = []
        low_data = []
<<<<<<< HEAD
        ech = 1
        x_data = [self.chart.startTime + ech*i*self.chart.period for i in range(0,int(1+(self.chart.endTime-self.chart.startTime)//(ech*self.chart.period)))]
=======
        x_data = []
>>>>>>> d72e5f3ae5b5e2531245d3e532fe25562102823e


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
             "xaxis" : {'ticks':"",'showticklabels':False,'ticktext': tt.FloattoTime(tab=x_data),'tickvals': x_data }
            }

        data = [trace]
        fig = dict(data=data, layout=layout)
        plotly.offline.plot(fig,filename='test_graphe.html')
