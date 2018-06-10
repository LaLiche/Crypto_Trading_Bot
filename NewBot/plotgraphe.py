import plotly
from botchart import BotChart
import timetranslate as tt
from botindicators import BotIndicators
from botstrategy import BotStrategy


class PlotGraphe(object):
    def __init__(self,chart,strategy):
        self.chart = chart
        self.strategy = strategy
        self.indicateurs = BotIndicators()


    def plotRsi(self,prices,temps):

        RSI_data = [50]
        for i in range(1,len(prices)):
            RSI_data.append(self.indicateurs.RSI(prices[:i]))
        RSI_data.append(50)

        rsi = plotly.graph_objs.Scatter(
        x = temps,
        y = RSI_data,
        marker = dict(size = 10,color = 'rgba(255, 0, 255, .9)')
        )

        rsi_min = plotly.graph_objs.Scatter(
        x = temps,
        y = [30 for i in range(len(temps))],
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        rsi_max = plotly.graph_objs.Scatter(
        x = temps,
        y = [70 for i in range(len(temps))],
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        return rsi,rsi_min,rsi_max


    def plotTrade(self,trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time):

        entryPoint = plotly.graph_objs.Scatter(
        x = trade_entry_time,
        y = trade_entry_data,
        mode = 'markers',
        marker = dict(size = 10,color = 'rgba(0, 255, 0, .9)')
        )

        exitPoint = plotly.graph_objs.Scatter(
        x = trade_exit_time,
        y = trade_exit_data,
        mode = 'markers',
        marker = dict(size = 10,color = 'rgba(255, 0, 0, .9)')
        )

        return entryPoint,exitPoint

    def plotPortfolio(self,trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time):

        portfolioValue = [trade_entry_data[0]]
        all_trade_time = [tt.FloattoTime(self.chart.startTime)]

        j = 0
        for i in range(len(trade_exit_data)):
            portfolioValue.append(portfolioValue[j]-trade_entry_data[i])
            all_trade_time.append(trade_entry_time[i])
            portfolioValue.append(portfolioValue[j+1]+trade_exit_data[i])
            all_trade_time.append(trade_exit_time[i])
            j += 2

        portfolio = plotly.graph_objs.Scatter(
        x = all_trade_time,
        y = portfolioValue,
        mode = 'lines+markets',
        marker = dict(size = 10,color = 'rgba(0, 0, 255, .9)')
        )
        return portfolio

    def plotCandle(self,open_data,close_data,high_data,low_data,x_data):

        trace = plotly.graph_objs.Candlestick(
            x = x_data,
            open = open_data,
            close = close_data,
            high = high_data,
            low = low_data)
        return trace

    def plotChart(self):

        open_data = []
        close_data = []
        high_data = []
        low_data = []
        x_data = []
        trade_entry_data = []
        trade_entry_time = []
        trade_exit_data = []
        trade_exit_time = []


        for c in self.chart.data:
            open_data.append(c.open)
            close_data.append(c.close)
            high_data.append(c.high)
            low_data.append(c.low)
            x_data.append(tt.FloattoTime(c.startTime))

        for trade in self.strategy.trades:
            trade_entry_data.append(trade.entryPrice*0.9)
            trade_entry_time.append(tt.FloattoTime(trade.startTime))
            if trade.exitTime != 0:
                trade_exit_data.append(trade.exitPrice*0.9)
                trade_exit_time.append(tt.FloattoTime(trade.exitTime))

        trace = self.plotCandle(open_data,close_data,high_data,low_data,x_data)
        rsi,rsi_min,rsi_max = self.plotRsi(close_data,x_data)
        entryPoint,exitPoint = self.plotTrade(trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time)
        portfolio = [self.plotPortfolio(trade_entry_data,trade_entry_time,trade_exit_data,trade_exit_time)]

        layout = {
            'title': self.chart.pair+" "+str(self.chart.period)+" s",
            'yaxis1': {'title': self.chart.pair,'domain':[0.26,1]},
            'yaxis2':{'domain':[0,0.25]},
            # 'xaxis2' : {'ticks':"",'showticklabels':False,'ticktext': tt.FloattoTime(tab=x_data),'tickvals': x_data, },
            # 'yaxis3':{'domain':[0.26,1]},
            # 'xaxis3' : {'ticks':"",'showticklabels':False,'ticktext': tt.FloattoTime(tab=x_data),'tickvals': x_data, },
            }

        fig = plotly.tools.make_subplots(rows=2, cols=1,shared_xaxes=True)
        fig.append_trace(trace, 1, 1)
        fig.append_trace(entryPoint, 1, 1)
        fig.append_trace(exitPoint, 1, 1)
        fig.append_trace(rsi, 2, 1)
        fig.append_trace(rsi_min, 2, 1)
        fig.append_trace(rsi_max, 2, 1)
        fig['layout']=layout
        plotly.offline.plot(fig,filename='graphe.html')
        plotly.offline.plot(portfolio,filename='portfolio.html')
