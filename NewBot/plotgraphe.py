import plotly
from botchart import BotChart
from poloniex import poloniex
import timetranslate as tt
from botindicators import BotIndicators


class PlotGraphe(object):
    def __init__(self,chart):
        self.chart = chart
        self.indicateurs = BotIndicators()


    def plotrsi(self,prices,temps):

        RSI_data = [50]
        for i in range(1,len(prices)):
            RSI_data.append(self.indicateurs.RSI(prices[:i]))
        RSI_data.append(50)

        rsi = plotly.graph_objs.Scatter(
        x = temps,
        y = RSI_data,
        )

        rsi_min = plotly.graph_objs.Scatter(
        x = temps,
        y = [30 for i in range(len(temps))]
        )

        rsi_max = plotly.graph_objs.Scatter(
        x = temps,
        y = [70 for i in range(len(temps))]
        )

        return rsi,rsi_min,rsi_max



    def plotcandle(self,open_data,close_data,high_data,low_data,x_data):

        trace = plotly.graph_objs.Candlestick(
            x = x_data,
            open = open_data,
            close = close_data,
            high = high_data,
            low = low_data)
        return trace

    def plotchart(self):

        # TODO ajouter strategies & indicateurs
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

        trace = self.plotcandle(open_data,close_data,high_data,low_data,x_data)
        rsi,rsi_min,rsi_max = self.plotrsi(close_data,x_data)

        layout = {
            'title': self.chart.pair+" "+str(self.chart.period)+" s",
            'yaxis1': {'title': self.chart.pair,'domain':[0.26,1]},
            'xaxis' : {'ticks':"",'showticklabels':False,'ticktext': tt.FloattoTime(tab=x_data),'tickvals': x_data, },
            'yaxis2':{'domain':[0,0.25]},
            'xaxis2' : {'ticks':"",'showticklabels':False,'ticktext': tt.FloattoTime(tab=x_data),'tickvals': x_data, },
            }

        fig = plotly.tools.make_subplots(rows=2, cols=1,shared_xaxes=True)
        fig.append_trace(trace, 1, 1)
        fig.append_trace(rsi, 2, 1)
        fig.append_trace(rsi_min, 2, 1)
        fig.append_trace(rsi_max, 2, 1)
        fig['layout']=layout
        plotly.offline.plot(fig,filename='test_graphe.html')
