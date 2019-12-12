from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QTabWidget, QGridLayout, QMainWindow
from .historymetrics import HistoryMetrics

class MainMetrics(QMainWindow):
    def __init__(self, allData={}):
        super().__init__()
        self.allData = allData
        self.setMinimumWidth(900)
        self.setMinimumHeight(500)
        self.setWindowTitle("metrics")
        self.buildUI()

    def loadData(self, data):
        self.allData = data
        self.buildUI()

    def getHistoryTab(self):
        self.historyLayout = HistoryMetrics(self.allData)
        historyTabWidget = QWidget()
        historyTabWidget.setLayout(self.historyLayout)
        return historyTabWidget

    def getCategoriesTab(self):
        label = QLabel('ayyy')
        return label

    def buildUI(self):
        self.metricsWrapperWidget = QWidget()
        self.setCentralWidget(self.metricsWrapperWidget)
        self.tabLayout = QGridLayout()
        self.tabWidget = QTabWidget()


        self.historyTab = self.getHistoryTab()
        self.categoriesTab = self.getCategoriesTab()

        self.tabWidget.addTab(self.historyTab, "History")
        self.tabWidget.addTab(self.categoriesTab, "Categories")

        self.tabLayout.addWidget(self.tabWidget, 0, 0)
        closeButton = self.buildCloseButton()
        self.tabLayout.addWidget(closeButton)
        self.metricsWrapperWidget.setLayout(self.tabLayout)

    def buildCloseButton(self):
        closeButton = QPushButton('close')
        closeButton.setShortcut('Ctrl+W')
        closeButton.clicked.connect(self.onClose)
        closeButton.setFixedSize(0, 0)
        return closeButton

    def onClose(self):
        self.hide()
        self.deleteLater()