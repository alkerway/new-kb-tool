from PySide2.QtWidgets import QWidget, QVBoxLayout

from kbutils import ConfigUtil
from .category import Category

class DataDisplay(QWidget):
    def __init__(self, transactionList, monthCode):
        QWidget.__init__(self)
        self.allTransactions = []
        self.configUtil = ConfigUtil()
        self.loadNewMonth(transactionList, monthCode)

    def addCategory(self, data):
        cfg = self.configUtil.getConfig()
        amt = int(data['amt'])
        cfg['months'][self.month][data['title']] = {
            'transactionList': [],
            'total': amt
        }
        self.configUtil.setConfig(cfg)

        idx = -1
        for i, section in enumerate(self.sectionState):
            if int(section['total']) < amt:
                idx = i
                break

        self.sectionState.insert(idx, {'name': data['title'], 'total': amt})
        self.contentWrapperLayout.insertWidget(idx, Category(data['title'], amt, []))
        # self.updateTotalAmt()

    def loadNewMonth(self, transactionList, monthCode, disableCredit=False):
        self.allTransactions = transactionList
        self.month = monthCode
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

        categoryKeys = list(formattedSections.keys())
        categoryKeys.sort(key=lambda x: formattedSections[x]['total'], reverse=True)
        sectionsUI = []
        self.sectionState = []
        for category in categoryKeys:
            if category == 'income':
              pass
            elif category == 'uncategorized':
                self.sectionState.append({'name': 'Uncategorized', 'total': '0'})
                sectionsUI.append(Category('Uncategorized', '0', formattedSections['uncategorized']['tList']))
            else:
                self.sectionState.append({'name': category, 'total': config['months'][monthCode][category]['total']})
                sectionsUI.append(Category(category, config['months'][monthCode][category]['total'], formattedSections[category]['tList']))

        self.contentWrapperLayout = QVBoxLayout()
        for sectionLayout in sectionsUI:
            print(sectionLayout)
            self.contentWrapperLayout.addWidget(sectionLayout)
        print(self.contentWrapperLayout, 'wrapperlayout')
        self.setLayout(self.contentWrapperLayout)
        print(config)
        self.configUtil.setConfig(config)

    def dropEvent(self, transactionTitle):
        cfg = self.configUtil.getConfig()
        sourceCat = self.getCategoryFromTransaction(cfg, transactionTitle)
        print(sourceCat)
        if not len(sourceCat) or sourceCat[0] != self.title:
            transactionsToAdd = []
            if len(sourceCat):
                oldList = cfg['months'][self.month][sourceCat[0]]['transactionList']
                newList = list(filter((transactionTitle).__ne__, oldList))
                cfg['months'][self.month][sourceCat[0]]['transactionList'] = newList
                # transactionsToAdd += self.wrapper.removeTransactionsFromCategory(transactionTitle, sourceCat[0])
            else:
                pass
                # transactionsToAdd += self.wrapper.removeTransactionsFromCategory(transactionTitle, 'Uncategorized')

            if self.title != 'Uncategorized':
                cfg['categories'][self.title]['transactionList'].append(transactionTitle)

            self.configUtil.setConfig(cfg)
            # self.addTransactions(transactionsToAdd)

    def getCategoryFromTransaction(self, cfg, title):
        category = list(filter(lambda x: title in cfg['months'][self.month][x]['transactionList'], cfg['months'][self.month].keys()))
        return category


    def getTotalAmt(self, transactionList):
        totalAmt = 0
        for transaction in transactionList:
            totalAmt += (-1 * transaction.amt) if transaction.isCredit else transaction.amt
        return str(round(totalAmt, 2))