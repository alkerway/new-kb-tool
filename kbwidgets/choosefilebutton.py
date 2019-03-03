from PySide2.QtWidgets import QPushButton

class ChooseFileButton(QPushButton):
    def __init__(self):
        QPushButton.__init__(self)
        self.clicked.connect(self.showFileSelect)
        self.setShortcut('Ctrl+O')
        self.setMaximumWidth(90)

    def showFileSelect(self):
        pass