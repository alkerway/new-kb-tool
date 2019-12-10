from PySide2.QtWidgets import QMainWindow

class MainMetrics(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(900)
        self.setWindowTitle("metrics")

    def loadData(self, data):
        print(data)