from PySide2.QtWidgets import QHBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class HistoryMetrics(QHBoxLayout):
    def __init__(self, allData):
        super().__init__()
        self.monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.allData = allData
        self.createPlot()

    def createPlot(self):
        xValues, xLabels, yValues = self.parseData(self.allData)
        fig = Figure(dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        axis = fig.add_subplot(111)
        axis.bar(xValues, yValues, tick_label=xLabels, color=(67/255, 160/255, 71/255))
        axis.set_ylabel('$')
        axis.set_xlabel('Month')
        canvas = FigureCanvas(fig)
        self.addWidget(canvas)

    def parseData(self, data):
        xLabels = []
        xValues = []
        yValues = []
        months = sorted(list(data.keys()))
        for idx in range(len(months)):
            key = months[idx]
            transactions = data[key]
            sumTransactions = self.getSumTransactions(transactions)
            xLabels.append(self.getMonthDisplay(key))
            xValues.append(idx)
            yValues.append(sumTransactions)
        return (xValues, xLabels, yValues)

    def getSumTransactions(self, transactions, income=False):
        # filter income etc
        return sum([i.amt for i in transactions if not i.isCredit])

    def getMonthDisplay(self, monthStr):
        year, month = monthStr.split('-')
        return '{:.3} \'{}'.format(self.monthNames[int(month) - 1], year[2:])