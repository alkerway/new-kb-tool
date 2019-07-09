from PySide2.QtWidgets import QProgressBar
from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt
import time
import asyncio

animate = False


class ProgressBar(QProgressBar):
    def __init__(self, isIncome=False):
        QProgressBar.__init__(self)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setMaximumWidth(300)
        self.isIncome = isIncome

    def updateValues(self, maxVal, value):
        oldValue = max(self.value(), 0)
        palette = QPalette(self.palette())
        greenColor = value > int(maxVal) if not self.isIncome else value < int(maxVal)
        if not greenColor:
            palette.setColor(QPalette.Highlight, QColor(Qt.darkGreen))
        else:
            palette.setColor(QPalette.Highlight, QColor(Qt.darkRed))
        self.setPalette(palette)
        self.setRange(0, max(value, int(maxVal)))
        self.setFormat('$' + str(round(value, 2)) + ' / ' + str(maxVal))

        if animate and oldValue != value:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.animateBar(oldValue, value, maxVal))
            loop.close()
        self.setValue(value)
        return self

    @asyncio.coroutine
    def animateBar(self, oldValue, newValue, maxVal):
        diff = newValue - oldValue
        sign = -1
        if diff >= 0:
            sign = 1

        currentValue = int(oldValue)
        counter = 0
        if abs(newValue - currentValue) > 0.01:
            while abs(newValue - currentValue) > 0.01:
                yield from asyncio.sleep(0.000001)
                currentValue = currentValue + diff / 1000
                if currentValue > maxVal:
                    break
                self.setValue(currentValue)
                counter = counter + 1
                if counter > 10000000:
                    print('breaking from counter at ' + str(currentValue))
                    break
