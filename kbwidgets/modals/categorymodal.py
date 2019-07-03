from PySide2.QtWidgets import QDialog, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PySide2.QtGui import QIntValidator
from PySide2 import QtCore


class CategoryModal(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setGeometry(125, 100, 0, 0)
        self.setModal(True)
        self.setWindowTitle('Add Category')
        self.show()

    def getData(self):
        inputTitle = QLabel('Title: ')
        self.inputEdit = QLineEdit()
        self.inputEditSs = self.inputEdit.styleSheet()
        self.inputEdit.textChanged.connect(lambda text: self.inputEdit.setStyleSheet(self.inputEditSs))
        self.inputEdit.setMaxLength(20)
        titleLayout = QHBoxLayout()
        titleLayout.addWidget(inputTitle)
        titleLayout.addWidget(self.inputEdit)

        amtTitle = QLabel('Amount: $')
        self.amtEdit = QLineEdit()
        self.amtEditSs = self.amtEdit.styleSheet()
        self.amtEdit.textChanged.connect(lambda text: self.amtEdit.setStyleSheet(self.amtEditSs))
        validator = QIntValidator(1, 9999, self)
        self.amtEdit.setValidator(validator)
        amtTitle.setMaximumWidth(120)
        self.amtEdit.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.amtEdit.returnPressed.connect(self.okClicked)
        amtLayout = QHBoxLayout()
        amtLayout.addWidget(amtTitle)
        amtLayout.addWidget(self.amtEdit)

        okButton = QPushButton('OK')
        okButton.clicked.connect(self.okClicked)
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(self.cancelClicked)
        buttons = QHBoxLayout()
        buttons.addWidget(cancelButton)
        buttons.addWidget(okButton)

        modalLayout = QVBoxLayout()
        modalLayout.addLayout(titleLayout)
        modalLayout.addLayout(amtLayout)
        modalLayout.addLayout(buttons)

        self.setLayout(modalLayout)
        retValue = self.exec()
        if retValue:
            return {'title': self.inputEdit.text(), 'amt': self.amtEdit.text()}
        else:
            return 0

    def okClicked(self):
        if not self.inputEdit.text():
            self.inputEdit.setStyleSheet("border: 2px solid red;")
            self.inputEdit.setFocus()
        elif not self.amtEdit.text():
            self.amtEdit.setStyleSheet("border: 2px solid red;")
            self.amtEdit.setFocus()
        else:
            self.accept()

    def cancelClicked(self):
        self.reject()