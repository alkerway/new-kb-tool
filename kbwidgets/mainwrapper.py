import sys

from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog
from PySide2.QtGui import QFont
from PySide2 import QtCore

from kbparsers import CSVParser
from .choosefilebutton import ChooseFileButton


boldFont = QFont()
boldFont.setBold(True)
boldFont.setPointSize(12)

class MainWrapper(QWidget):
    def __init__(self):
        super(MainWrapper, self).__init__()
        self.buildUI()

    def showFileSelect(self):
        fname, success = QFileDialog.getOpenFileName(None, 'Open CSV Statement', '', 'CSV (*.csv *.CSV)')
        if success:
            parser = CSVParser()
            formatted = parser.parseCsv(fname)
                # self.transactions = formatted
                # self.sumTransactions = 0
                # for t in self.transactions:
                #     self.sumTransactions += float(t.amt)
                # self.generateContentUI()

    def buildUI(self):
        self.closeButton = QPushButton('close')
        self.closeButton.setShortcut('Ctrl+W')
        self.closeButton.clicked.connect(self.closeApp)
        self.closeButton.setFixedSize(0, 0)

        self.buildTitleLayout()
        self.buildMonthDisplayLayout()
        self.buildHeaderWidget()

        self.mainWrapperLayout = QVBoxLayout()
        self.mainWrapperLayout.addLayout(self.titleLayout)
        self.mainWrapperLayout.addLayout(self.monthDisplayLayout)
        self.mainWrapperLayout.addWidget(self.headerWidget)
        self.mainWrapperLayout.addWidget(self.closeButton)

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
        self.monthTitle.setText('Month')
        self.monthTitle.setMaximumWidth(75)
        self.monthTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.monthIncreaseButton = QPushButton('>')
        self.monthDecreaseButton = QPushButton('<')
        self.monthIncreaseButton.setMaximumWidth(20)
        self.monthDecreaseButton.setMaximumWidth(20)

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
        # self.categoriesAddButton.clicked.connect(self.promptAddCategory)
        self.categoriesAddButton.setToolTip('Add Category')

        self.sumTransactions = 0
        self.totalDisplay = QLabel(self)
        self.totalDisplay.setText('Total: - / -')
        self.totalDisplay.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.totalDisplay.setFont(boldFont)


        self.headerLayout = QHBoxLayout()
        self.headerLayout.addWidget(self.categoriesTitle)
        self.headerLayout.addWidget(self.categoriesAddButton)
        self.headerLayout.addWidget(self.totalDisplay)
        self.headerLayout.setMargin(0)

        self.headerWidget = QWidget()
        self.headerWidget.setLayout(self.headerLayout)

        minSize = self.headerLayout.minimumSize()
        minSize.setWidth(450)
        self.headerWidget.setMaximumSize(minSize)

    def closeApp(self):
        sys.exit()

