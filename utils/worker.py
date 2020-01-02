import time
from functools import partial
from PySide2 import QtCore


class SeparateThread(QtCore.QThread):
    finished = QtCore.Signal(object)
    def startFunc(self, func, *args):
        self.worker = Worker()
        self.worker.moveToThread(self)
        self.started.connect(partial(self.worker.runFunc, func, *args))
        self.start()
        self.worker.finished.connect(self.onFinished)

    def onFinished(self, output):
        self.finished.emit(output)
        self.quit()


class Worker(QtCore.QObject):
    processed = QtCore.Signal(int)
    finished = QtCore.Signal(object)

    def runFunc(self, func, *args):
        output = func(*args)
        self.finished.emit(output)