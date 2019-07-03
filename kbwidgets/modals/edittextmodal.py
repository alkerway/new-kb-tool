from PySide2.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PySide2.QtGui import QIntValidator, QRegExpValidator
from PySide2 import QtCore
import re

class EditTextModal(QDialog):
    def __init__(self, oldText, windowTitle):
        QDialog.__init__(self)
        self.setGeometry(125, 100, 200, 0)
        self.setModal(True)
        self.setWindowTitle(windowTitle)
        self.oldText = oldText
        self.show()
    
    def getData(self):

        titleLabel = QLabel('Title: ')

        self.titleEdit = QLineEdit()
        self.titleEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.titleEditSs = self.titleEdit.styleSheet()
        self.titleEdit.textChanged.connect(lambda text: self.titleEdit.setStyleSheet(self.titleEditSs))
        self.titleEdit.setMaxLength(20)
        self.titleEdit.returnPressed.connect(self.okClicked)
        self.titleEdit.setText(self.oldText)
        self.titleEdit.selectAll()

        okButton = QPushButton('OK')
        okButton.clicked.connect(self.okClicked)

        menuLayout = QVBoxLayout()

        topLine = QHBoxLayout()
        topLine.addWidget(titleLabel)
        topLine.addWidget(self.titleEdit)

        menuLayout.addLayout(topLine)
        menuLayout.addWidget(okButton)

        self.setLayout(menuLayout)
        retValue = self.exec()
        if retValue:
            return self.titleEdit.text()
        else:
            return 0
    
    def okClicked(self):
        validator = re.compile('.*\S.*')
        if not re.match(validator, self.titleEdit.text()):
            self.titleEdit.setStyleSheet("border: 2px solid red;")
        else:
            self.accept()
    
    def cancelClicked(self):
        self.reject()