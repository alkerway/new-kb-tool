from PySide2.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
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
        csvParser = CSVParser()
        csvParser.parseCsv('out.csv')

    def buildUI(self):
        self.appTitle = QLabel(self)
        self.appTitle.setText("App Title")
        self.appTitle.setFont(boldFont)

        self.chooseFileButton = QPushButton("choose file")
        # self.chooseFileButton.clicked.connect(self.showFileSelect)
        self.chooseFileButton.setShortcut('Ctrl+O')
        self.chooseFileButton.setMaximumWidth(90)

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

        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.appTitle)
        self.titleLayout.addWidget(self.chooseFileButton)

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

        self.mainWrapperLayout = QVBoxLayout()
        self.mainWrapperLayout.addLayout(self.titleLayout)
        self.mainWrapperLayout.addWidget(self.headerWidget)

        self.setLayout(self.mainWrapperLayout)

        self.setMinimumWidth(450)

