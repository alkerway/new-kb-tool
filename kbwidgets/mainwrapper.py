import sys

from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog, QScrollArea, QFrame, QSizePolicy
from PySide2.QtGui import QFont
from PySide2 import QtCore

from kbparsers import CSVParser
from kbutils import clearLayout
from kbwidgets.modals import CategoryModal
from .datadisplay import DataDisplay
from kbstate import State, Events

boldFont = QFont()
boldFont.setBold(True)
boldFont.setPointSize(12)

class MainWrapper(QWidget):
    def __init__(self):
        super(MainWrapper, self).__init__()
        self.monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.state = State()
        self.addListeners()
        self.buildUI()
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

    def showFileSelect(self):
        fname, success = QFileDialog.getOpenFileName(None, 'Open CSV Statement', '', 'CSV (*.csv *.CSV)')
        if success:
            parser = CSVParser()
            self.transactionMap = parser.parseCsv(fname)
            allMonths = list(self.transactionMap.keys())
            allMonths.sort()
            self.monthsList = allMonths
            self.loadMonth(allMonths[-1])
            if len(allMonths) > 1:
                self.monthDecreaseButton.show()

    def addListeners(self):
        self.state.addSubscriber(Events.update_total, self.setTotalDisplay)

    def loadMonth(self, monthText):
        monthNumber = int(monthText.split('-')[1])
        self.monthTitle.setText(self.monthNames[monthNumber - 1] + ' ' + monthText.split('-')[0])
        prevCode = None if self.currentMonth == 'Month' else self.currentMonth
        self.currentMonth = monthText
        clearLayout(self.dataDisplayWrapper)
        self.dataDisplay = DataDisplay(self.state,
                                       self.transactionMap[self.currentMonth],
                                       self.currentMonth,
                                       prevCode=prevCode)
        self.dataDisplay.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)

        self.dataDisplayWrapper.addWidget(self.dataDisplay)

    def loadPreviousMonth(self):
        currentIndex = self.monthsList.index(self.currentMonth)
        if currentIndex > 0:
            newMonth = self.monthsList[currentIndex - 1]
            self.loadMonth(newMonth)
            self.monthIncreaseButton.show()
            if currentIndex == 1:
                self.monthDecreaseButton.hide()


    def loadNextMonth(self):
        currentIndex = self.monthsList.index(self.currentMonth)
        if currentIndex < len(self.monthsList) - 1:
            newMonth = self.monthsList[currentIndex + 1]
            self.loadMonth(newMonth)
            self.monthDecreaseButton.show()
            if currentIndex == len(self.monthsList) - 2:
                self.monthIncreaseButton.hide()

    def setTotalDisplay(self, transactionTotal, categoryTotal):
        self.totalDisplay.setText('Total: $' + str(transactionTotal) + ' / ' + str(categoryTotal))
        if transactionTotal <= categoryTotal:
            self.totalDisplay.setStyleSheet("QLabel { color : darkGreen; }")
        else:
            self.totalDisplay.setStyleSheet("QLabel { color : darkRed; }")

    def buildUI(self):
        self.closeButton = QPushButton('close')
        self.closeButton.setShortcut('Ctrl+W')
        self.closeButton.clicked.connect(self.closeApp)
        self.closeButton.setFixedSize(0, 0)

        self.buildTitleLayout()
        self.buildMonthDisplayLayout()
        self.buildHeaderWidget()

        self.headerLayout = QVBoxLayout()
        self.headerLayout.addLayout(self.titleLayout)
        self.headerLayout.addLayout(self.monthDisplayLayout)
        self.headerLayout.addWidget(self.categoryHeaderWidget)
        self.headerLayout.addWidget(self.closeButton)

        self.headerLayoutWrapperWidget = QWidget()
        self.headerLayoutWrapperWidget.setLayout(self.headerLayout)
        self.headerLayoutWrapperWidget.setMaximumHeight(100)

        self.dataDisplayWrapper = QHBoxLayout()

        self.mainWrapperLayout = QVBoxLayout()
        self.mainWrapperLayout.addWidget(self.headerLayoutWrapperWidget)
        self.mainWrapperLayout.addLayout(self.dataDisplayWrapper)

        self.setLayout(self.mainWrapperLayout)

        self.setMinimumWidth(450)

    def buildTitleLayout(self):
        self.appTitle = QLabel(self)
        self.appTitle.setText("App Title")
        self.appTitle.setFont(boldFont)

        self.chooseFileButton = QPushButton("choose file")
        self.chooseFileButton.clicked.connect(self.showFileSelect)
        self.chooseFileButton.setShortcut('Ctrl+O')
        self.chooseFileButton.setMaximumWidth(90)

        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.appTitle)
        self.titleLayout.addWidget(self.chooseFileButton)

    def buildMonthDisplayLayout(self):
        self.monthTitle = QLabel(self)
        self.currentMonth = 'Month'
        self.monthTitle.setText(self.currentMonth)
        self.monthTitle.setMaximumWidth(115)
        self.monthTitle.setAlignment(QtCore.Qt.AlignCenter)

        self.monthIncreaseButton = QPushButton('>')
        self.monthIncreaseButton.clicked.connect(self.loadNextMonth)
        self.monthDecreaseButton = QPushButton('<')
        self.monthDecreaseButton.clicked.connect(self.loadPreviousMonth)
        self.monthIncreaseButton.setMaximumWidth(20)
        self.monthDecreaseButton.setMaximumWidth(20)
        self.monthIncreaseButton.hide()
        self.monthDecreaseButton.hide()

        self.monthDisplayWrapper = QHBoxLayout()
        self.monthDisplayWrapper.addWidget(self.monthDecreaseButton)
        self.monthDisplayWrapper.addWidget(self.monthTitle)
        self.monthDisplayWrapper.addWidget(self.monthIncreaseButton)

        self.monthDisplayLayout = QHBoxLayout()
        self.monthDisplayLayout.addLayout(self.monthDisplayWrapper)

    def buildHeaderWidget(self):
        self.categoriesTitle = QLabel(self)
        self.categoriesTitle.setText('Categories')
        self.categoriesTitle.setMaximumWidth(88)
        self.categoriesTitle.setFont(boldFont)

        self.categoriesAddButton = QPushButton('+')
        self.categoriesAddButton.setMaximumWidth(20)
        self.categoriesAddButton.clicked.connect(self.promptAddCategory)
        self.categoriesAddButton.setToolTip('Add Category')

        self.sumTransactions = 0
        self.totalDisplay = QLabel(self)
        self.totalDisplay.setText('Total: - / -')
        self.totalDisplay.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.totalDisplay.setFont(boldFont)


        self.categoryHeaderLayout = QHBoxLayout()
        self.categoryHeaderLayout.addWidget(self.categoriesTitle)
        self.categoryHeaderLayout.addWidget(self.categoriesAddButton)
        self.categoryHeaderLayout.addWidget(self.totalDisplay)
        self.categoryHeaderLayout.setMargin(0)

        self.categoryHeaderWidget = QWidget()
        self.categoryHeaderWidget.setLayout(self.categoryHeaderLayout)

        minSize = self.categoryHeaderLayout.minimumSize()
        minSize.setWidth(450)
        self.categoryHeaderWidget.setMaximumSize(minSize)

    def promptAddCategory(self):
        modal = CategoryModal()
        data = modal.getData()
        if data:
            self.state.next(Events.add_category, data)

    def closeApp(self):
        sys.exit()

