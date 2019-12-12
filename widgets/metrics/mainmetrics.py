from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QTabWidget, QVBoxLayout, QMainWindow, QDateEdit, QHBoxLayout
from PySide2 import QtCore
from .historymetrics import HistoryMetrics
from datetime import date

from state import State, Events

class MainMetrics(QMainWindow):
    def __init__(self, state, allData={}):
        super().__init__()
        self.state = state
        self.allData = allData
        self.dataSubset = allData
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
        self.tabLayout = QVBoxLayout()
        self.tabWidget = QTabWidget()
        self.dateRangeContainer = self.getDateRangeLine()
        self.dateRangeContainer.setMaximumWidth(425)

        self.historyTab = self.getHistoryTab()
        self.categoriesTab = self.getCategoriesTab()

        self.tabWidget.addTab(self.historyTab, "History")
        self.tabWidget.addTab(self.categoriesTab, "Categories")

        self.tabLayout.addWidget(self.dateRangeContainer)
        self.tabLayout.addWidget(self.tabWidget, 0, 0)
        closeButton = self.buildCloseButton()
        self.tabLayout.addWidget(closeButton)
        self.metricsWrapperWidget.setLayout(self.tabLayout)

    def getDateRangeWidget(self, minDate, maxDate):
        dateRange = QDateEdit()
        dateRange.setCalendarPopup(True)
        dateRange.setDisplayFormat('dd/MM/yyyy')
        dateRange.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        dateRange.setMaximumDate(maxDate)
        dateRange.setMinimumDate(minDate)
        return dateRange

    def getDateRangeLine(self):
        dateRangeLine = QWidget()
        dateRangeContainer = QHBoxLayout()
        minDate, maxDate = self.getFirstAndLastTransactionDates()
        self.startDatePicker = self.getDateRangeWidget(minDate, maxDate)
        self.startDatePicker.setDate(minDate)
        self.endDatePicker = self.getDateRangeWidget(minDate, maxDate)
        self.endDatePicker.setDate(maxDate)

        self.fromLabel = QLabel('Range:')
        self.toLabel = QLabel(' to ')

        self.dateUpdateButton = QPushButton('Update')
        self.dateUpdateButton.clicked.connect(self.updateDates)

        dateRangeContainer.addWidget(self.fromLabel)
        dateRangeContainer.addWidget(self.startDatePicker)
        dateRangeContainer.addWidget(self.toLabel)
        dateRangeContainer.addWidget(self.endDatePicker)
        dateRangeContainer.addWidget(self.dateUpdateButton)

        dateRangeLine.setLayout(dateRangeContainer)
        return dateRangeLine

    def getFirstAndLastTransactionDates(self):
        keys = list(filter(lambda k: len(self.allData[k]) > 0, sorted(list(self.allData.keys()))))
        if len(keys) == 0:
            return QtCore.QDate(0, 0, 0), QtCore.QDate(0, 0, 0)

        minDate = min(self.allData[keys[0]], key=lambda t: t.date).date
        maxDate = max(self.allData[keys[-1]], key=lambda t: t.date).date
        return QtCore.QDate(minDate.year, minDate.month, minDate.day), QtCore.QDate(maxDate.year, maxDate.month, maxDate.day)

    def updateDates(self):
        newData = {}
        qStartDate = self.startDatePicker.date()
        qEndDate = self.endDatePicker.date()
        startDate = date(qStartDate.year(), qStartDate.month(), qStartDate.day())
        endDate = date(qEndDate.year(), qEndDate.month(), qEndDate.day())
        for key in list(self.allData.keys()):
            keyYear, keyMonth = [int(k) for k in key.split('-')]
            if keyYear < startDate.year or keyYear > endDate.year:
                continue
            if keyMonth < startDate.month or keyMonth > endDate.month:
                continue
            newData[key] = list(filter(lambda t: t.date >= startDate and t.date <= endDate, self.allData[key]))
        self.dataSubset = newData
        self.historyLayout.updateData(self.dataSubset)




    def buildCloseButton(self):
        closeButton = QPushButton('close')
        closeButton.setShortcut('Ctrl+W')
        closeButton.clicked.connect(self.onClose)
        closeButton.setFixedSize(0, 0)
        return closeButton

    def onClose(self):
        self.state.next(Events.metrics_close)