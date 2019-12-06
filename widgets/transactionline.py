from PySide2.QtWidgets import QHBoxLayout, QWidget, QLabel
from PySide2 import QtCore, QtGui

class TransactionLine(QWidget):
    def __init__(self, transaction):
        QWidget.__init__(self)
        transactionLine = QHBoxLayout()
        self.transaction = transaction

        self.tTitle = QLabel(self)
        self.tTitle.setText(transaction.displayName)
        self.tTitle.setMinimumWidth(290)

        tAmt = QLabel(self)
        tAmt.setText(str(round(transaction.amt, 2)))
        tAmt.setAlignment(QtCore.Qt.AlignRight)
        tAmt.setMaximumWidth(52)

        tDate = QLabel(self)
        tDate.setText(str(transaction.date.day))
        tDate.setAlignment(QtCore.Qt.AlignRight)
        tDate.setMaximumWidth(50)

        transactionLine.addWidget(self.tTitle)
        transactionLine.addWidget(tDate)
        transactionLine.addWidget(tAmt)

        transactionLine.setMargin(0)

        self.setLayout(transactionLine)
        if not self.transaction.isCredit:
            self.setCursor(QtCore.Qt.OpenHandCursor)

    def updateName(self, newName):
        self.transaction.displayName = newName
        self.tTitle.setText(newName)

    def mouseMoveEvent(self, event):
        if not self.transaction.isCredit:
            mimeData = QtCore.QMimeData()
            mimeData.setText(self.transaction.name)
            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(QtCore.Qt.MoveAction)