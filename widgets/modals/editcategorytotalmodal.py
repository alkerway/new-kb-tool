from PySide2.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide2.QtGui import QIntValidator
from PySide2 import QtCore

class EditCategoryTotalModal(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setGeometry(125, 100, 0, 0)
        self.setModal(True)
        self.setWindowTitle('Edit Total')
        self.show()
    
    def getData(self, currentAmount):

        amtTitle = QLabel('Total: $')
        amtTitle.setMaximumWidth(120)

        validator = QIntValidator(1, 99999, self)

        amtEdit = QLineEdit()
        amtEdit.setValidator(validator)
        amtEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        amtEdit.returnPressed.connect(self.okClicked)
        amtEdit.setText(str(currentAmount))
        amtEdit.selectAll()

        okButton = QPushButton('OK')
        okButton.clicked.connect(self.okClicked)

        amtLayout = QHBoxLayout()
        amtLayout.addWidget(amtTitle)
        amtLayout.addWidget(amtEdit)
        amtLayout.addWidget(okButton)

        self.setLayout(amtLayout)
        retValue = self.exec()
        if retValue:
            return amtEdit.text()
        else:
            return 0
    
    def okClicked(self):
        self.accept()
    
    def cancelClicked(self):
        self.reject()