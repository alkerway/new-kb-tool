from PySide2.QtWidgets import QHBoxLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class CategoryMetrics(QHBoxLayout):
    def __init__(self, state, data):
        super().__init__()
        self.state = state
        self.data = data
        self.createPlot()

    def createPlot(self):
        fig = Figure(dpi=72, facecolor=(1, 1, 1), edgecolor=(0, 0, 0))
        self.axis = fig.add_subplot(111)
        self.canvas = FigureCanvas(fig)
        amounts, labels = self.parseData(self.data)
        self.axis.pie(amounts, labels=labels, shadow=True)
        self.addWidget(self.canvas)

    def parseData(self, data):
        categoryList = self.getCategorieslist()
        labels = list(categoryList.keys())
        labels = ['{} (${:.0f})'.format(k, categoryList[k]) for k in labels]
        totalAmount = sum(list(categoryList.values()))
        proportionalCategories = [a/totalAmount for a in list(categoryList.values())]
        return proportionalCategories, labels

    def getCategorieslist(self):
        config = self.state.getConfig()
        months = sorted(list(self.data.keys()))
        categories = {}
        for month in months:
            monthTransactions = self.data[month]
            monthCat = list(config['months'][month].keys())
            for category in monthCat:
                tList = config['months'][month][category]['transactionList']
                if category == 'Income':
                    continue
                    # categorySum = sum(map(lambda t: t.isCredit and t.amt or 0, monthTransactions))
                else:
                    categorySum = sum(map(lambda t: t.name in tList and t.amt or 0, monthTransactions))
                if category in categories:
                    categories[category] += categorySum
                else:
                    categories[category] = categorySum
        return categories

    def updateData(self, data):
        self.data = data
        self.canvas.deleteLater()
        self.createPlot()