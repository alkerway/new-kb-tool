from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

class HistoryMetrics(QtGui.QHBoxLayout):
    def __init__(self, allData):
        super().__init__()
        self.allData = allData
        self.graphicsWindow = pg.GraphicsWindow(title="test graphics wiondow")
        self.addWidget(self.graphicsWindow)
        self.createPlot()

    def createPlot(self):
        xValues, xLabels, yValues = self.parseData(self.allData)
        x = xValues
        y = yValues
        # create bar chart
        print(xLabels)
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks(xLabels)
        plot1 = self.graphicsWindow.addPlot(axisItems={'bottom': stringaxis})
        plot1.setMouseEnabled(x=False, y=False)
        barGraph = pg.BarGraphItem(x=x, height=y, width=0.6, brush='b')
        plot1.addItem(barGraph)

    def parseData(self, data):
        xLabels = []
        xValues = []
        yValues = []
        months = sorted(list(data.keys()))
        for idx in range(len(months)):
            key = months[idx]
            transactions = data[key]
            sumTransactions = self.getSumTransactions(transactions)
            xLabels.append(key)
            xValues.append(idx)
            yValues.append(sumTransactions)
        return (xValues, xLabels, yValues)

    def getSumTransactions(self, transactions, income=False):
        # filter income etc
        return sum([i.amt for i in transactions if not i.isCredit])