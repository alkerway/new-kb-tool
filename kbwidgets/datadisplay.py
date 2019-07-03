from PySide2.QtWidgets import QWidget, QVBoxLayout

from kbutils import ConfigUtil
from .category import Category

class DataDisplay(QWidget):
    def __init__(self, state, transactionList, monthCode):
        QWidget.__init__(self)
        self.allTransactions = []
        self.configUtil = ConfigUtil(state)
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
        self.contentWrapperLayout.insertWidget(idx, Category(data['title'], amt, [], self))
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
                sectionsUI.append(Category('Uncategorized', '0', formattedSections['uncategorized']['tList'], self))
            else:
                self.sectionState.append({'name': category, 'total': config['months'][monthCode][category]['total']})
                sectionsUI.append(Category(category, config['months'][monthCode][category]['total'], formattedSections[category]['tList'], self))

        self.contentWrapperLayout = QVBoxLayout()
        for sectionLayout in sectionsUI:
            print(sectionLayout)
            self.contentWrapperLayout.addWidget(sectionLayout)
        print(self.contentWrapperLayout, 'wrapperlayout')
        self.setLayout(self.contentWrapperLayout)
        self.configUtil.setConfig(config)

    def updateConfigCategoryTotal(self, name, amt):
        cfg = self.configUtil.getConfig()
        cfg['months'][self.month][name]['total'] = amt
        self.configUtil.setConfig(cfg)

    def updateConfigCategoryName(self, name, newTitle):
        cfg = self.configUtil.getConfig()
        cfg['months'][self.month][newTitle] = cfg['months'][self.month].pop(name)
        self.configUtil.setConfig(cfg)

    def dropEvent(self, transactionTitle, destCategoryTitle):
        cfg = self.configUtil.getConfig()
        sourceCat = self.getCategoryFromTransaction(cfg, transactionTitle)
        if not len(sourceCat) or sourceCat[0] != destCategoryTitle:
            transactionsToAdd = []
            if len(sourceCat):
                oldList = cfg['months'][self.month][sourceCat[0]]['transactionList']
                newList = list(filter((transactionTitle).__ne__, oldList))
                cfg['months'][self.month][sourceCat[0]]['transactionList'] = newList
                transactionsToAdd += self.removeTransactionsFromCategory(transactionTitle, sourceCat[0])
            else:
                transactionsToAdd += self.removeTransactionsFromCategory(transactionTitle, 'Uncategorized')

            if destCategoryTitle != 'Uncategorized':
                cfg['months'][self.month][destCategoryTitle]['transactionList'].append(transactionTitle)

            self.configUtil.setConfig(cfg)
            categoryToAddTo = self.getCategoryWidget(destCategoryTitle)
            categoryToAddTo.addTransactions(transactionsToAdd)

    def removeTransactionsFromCategory(self, transactionTitle, title):
        i = 0
        transactionsRemoved = []
        curWidget = self.getCategoryWidget(title)
        j = 0
        while j < len(curWidget.transactions):
            widgetTransaction = curWidget.transactions[j]
            if widgetTransaction.name == transactionTitle:
                transactionsRemoved.append(widgetTransaction)
                curWidget.removeTransaction(widgetTransaction)
            else:
                j += 1

        return transactionsRemoved

    def getCategoryWidget(self, categoryName):
        i = 0
        curWidget = self.contentWrapperLayout.itemAt(i)
        while (curWidget):
            if curWidget.widget().name == categoryName:
                return curWidget.widget()
            i += 1
            curWidget = self.contentWrapperLayout.itemAt(i)

    def getCategoryFromTransaction(self, cfg, title):
        category = list(filter(lambda x: title in cfg['months'][self.month][x]['transactionList'], cfg['months'][self.month].keys()))
        return category

    def removeCategory(self, title, transactionList):
        cfg = self.configUtil.getConfig()

        amt = cfg['months'][self.month][title]['total']
        del cfg['months'][self.month][title]

        self.configUtil.setConfig(cfg)
        i = 0
        curWidget = self.contentWrapperLayout.itemAt(i)
        while (curWidget):
            if curWidget.widget().name == title:
                curWidget.widget().deleteLater()
                self.contentWrapperLayout.removeWidget(curWidget.widget())
                self.sectionState.remove({'name': title, 'total': amt})
            elif curWidget.widget().name == 'Uncategorized':
                curWidget.widget().addTransactions(transactionList)
                i += 1
            else:
                i += 1
            curWidget = self.contentWrapperLayout.itemAt(i)
        # self.updateTotalAmt()


    def getTotalAmt(self, transactionList):
        totalAmt = 0
        for transaction in transactionList:
            totalAmt += (-1 * transaction.amt) if transaction.isCredit else transaction.amt
        return str(round(totalAmt, 2))