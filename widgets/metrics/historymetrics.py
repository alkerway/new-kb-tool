from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from functools import reduce

class HistoryMetrics(QVBoxLayout):
    def __init__(self, state, data):
        super().__init__()
        self.monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.state = state
        self.data = data
        self.canvas = None
        self.createCategoryDropdown()
        self.createPlot()

    def updateData(self, newData):
        self.data = newData
        self.canvas.deleteLater()
        self.createPlot()

    def createCategoryDropdown(self):
        dropdownWrapperLayout = QHBoxLayout()
        dropdown = QComboBox()
        dropdown.addItem('All Expenses')
        dropdown.addItem('All Income')
        allCategories = self.getOrderedCategories()
        for category in allCategories:
            dropdown.addItem(category)
        dropdown.setMaximumWidth(200)
        dropdownWrapperLayout.addWidget(dropdown)
        self.addLayout(dropdownWrapperLayout)


    def createPlot(self):
        fig = Figure(dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.axis = fig.add_subplot(111)
        self.axis.set_ylabel('$')
        self.axis.set_xlabel('Month')
        self.canvas = FigureCanvas(fig)
        xValues, xLabels, yValues = self.parseData(self.data)
        self.axis.bar(xValues, yValues, tick_label=xLabels, color=(67 / 255, 160 / 255, 71 / 255))
        self.addWidget(self.canvas)

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

    def getOrderedCategories(self):
        config = self.state.getConfig()
        frequencies = {}
        categories = []
        for month in list(config['months'].keys()):
            for category in list(config['months'][month].keys()):
                if category not in categories:
                    categories.append(category)
                    frequencies[category] = 1
                else:
                    frequencies[category] += 1
        categories.sort(key=lambda c: frequencies[c], reverse=True)
        return categories