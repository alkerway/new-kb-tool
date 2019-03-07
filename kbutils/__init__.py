from .transaction import Transaction
from .config import ConfigUtil


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()
        elif child.layout():
            clearLayout(child.layout())
            child.layout().setParent(None)