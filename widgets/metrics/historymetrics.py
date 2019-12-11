from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

class HistoryMetrics(QtGui.QHBoxLayout):
    def __init__(self):
        super().__init__()

        self.graphicsWindow = pg.GraphicsWindow(title="test graphics wiondow")
        self.createPlot()
        self.addWidget(self.graphicsWindow)

    def createPlot(self):
        x = range(-3, 2)
        y = [1, 2, 3, 4, 5]
        # create bar chart
        plot1 = self.graphicsWindow.addPlot()
        barGraph = pg.BarGraphItem(x=x, height=y, width=0.6, brush='b')
        plot1.addItem(barGraph)
        barGraph.set