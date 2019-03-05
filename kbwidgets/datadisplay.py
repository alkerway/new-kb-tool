from PySide2.QtWidgets import QHBoxLayout

from kbutils import ConfigUtil

class DataDisplay(QHBoxLayout):
    def __init__(self):
        super(DataDisplay, self).__init__()
        self.allTransactions = []
        self.configUtil = ConfigUtil()

    def addCategory(self):
        pass

    def loadNewMonth(self, transactionList, monthCode, disableCredit=False):
        self.allTransactions = transactionList
        self.month = monthCode
        self.clearLayout(self)
        self.constructCategories(transactionList, monthCode)

    def constructCategories(self, transactionList, monthCode):
        config = self.configUtil.getConfig()
        if not monthCode in config['months']:
            config['months'][monthCode] = {}

        formattedSections = {
            'uncategorized': {
                'tList': [],
                'total': 0
            },
            'income': {
                'tList': [],
                'total': 0
            }
        }

        for transaction in transactionList:
            foundCategory = False
            if transaction.isCredit:
                formattedSections['income']['tList'].append(transaction)
                formattedSections['income']['total'] += transaction.amt
            else:
                for category in list(config['months'][monthCode].keys()):
                    transactionList = config['months'][monthCode][category]['transactionList']
                    if not category in formattedSections.keys():
                        formattedSections[category] = {
                            'tList': [],
                            'total': config['months'][monthCode][category]['total']
                        }
                    if transaction.name in transactionList:
                        foundCategory = True
                        formattedSections[category]['tList'].append(transaction)
                        formattedSections[category]['total'] += transaction.amt
                if not foundCategory:
                    formattedSections['uncategorized']['tList'].append(transaction)
        print(formattedSections)

    def getTotalAmt(self, transactionList):
        totalAmt = 0
        for transaction in transactionList:
            totalAmt += (-1 * transaction.amt) if transaction.isCredit else transaction.amt
        return str(round(totalAmt, 2))

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clearLayout(child.layout())
                child.layout().setParent(None)