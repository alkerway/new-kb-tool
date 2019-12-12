from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QComboBox
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from functools import reduce

class HistoryMetrics(QVBoxLayout):
    def __init__(self, state, allData):
        super().__init__()
        self.monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.state = state
        self.allData = allData
        self.currentCategory = 'All Expenses'
        self.canvas = None
        self.createCategoryDropdown()
        self.createPlot()

    def updateData(self, newData):
        self.allData = newData
        self.canvas.deleteLater()
        self.createPlot()

    def createCategoryDropdown(self):
        dropdownWrapperLayout = QHBoxLayout()
        self.categoryDropdown = QComboBox()
        self.categoryDropdown.addItem('All Expenses')
        self.categoryDropdown.addItem('All Income')
        allCategories = self.getOrderedCategories()
        for category in allCategories:
            self.categoryDropdown.addItem(category)
        self.categoryDropdown.setMaximumWidth(200)
        self.categoryDropdown.currentIndexChanged.connect(self.onCategoryChange)
        dropdownWrapperLayout.addWidget(self.categoryDropdown)
        self.addLayout(dropdownWrapperLayout)

    def onCategoryChange(self):
        self.currentCategory = self.categoryDropdown.currentText()
        self.updateData(self.allData)

    def createPlot(self):
        fig = Figure(dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.axis = fig.add_subplot(111)
        self.axis.set_ylabel('$ {}'.format(self.currentCategory))
        self.axis.set_xlabel('Month')
        self.canvas = FigureCanvas(fig)
        xValues, xLabels, yValues = self.parseData(self.allData)
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
            sumTransactions = 54 # self.getSumTransactions(transactions, months[idx])
            xLabels.append(self.getMonthDisplay(key))
            xValues.append(idx)
            yValues.append(sumTransactions)
        return (xValues, xLabels, yValues)

    def getSumTransactions(self, transactions, month):
        # filter income etc
        config = self.state.getConfig()
        total = 0
        for transaction in transactions:
            if self.currentCategory == 'All Expenses':
                total += transaction.amt if not transaction.isCredit else 0
            elif self.currentCategory == 'All Income':
                total += transaction.amt if transaction.isCredit else 0
            elif self.currentCategory in config['months'][month] and \
                    transaction.name in config['months'][month][self.currentCategory]['transactionList']:
                total += transaction.amt
        return total

    def getMonthDisplay(self, monthStr):
        year, month = monthStr.split('-')
        return '{:.3} \'{}'.format(self.monthNames[int(month) - 1], year[2:])

    def getOrderedCategories(self):
        config = self.state.getConfig()
        frequencies = {}
        categories = []
        for month in list(config['months'].keys()):
            for category in list(config['months'][month].keys()):
                if category == 'Income':
                    continue
                if category not in categories:
                    categories.append(category)
                    frequencies[category] = 1
                else:
                    frequencies[category] += 1
        categories.sort(key=lambda c: frequencies[c], reverse=True)
        return categories