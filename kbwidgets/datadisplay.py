from PySide2.QtWidgets import QWidget, QVBoxLayout

from kbstate import Events
from .category import Category

class DataDisplay(QWidget):
    def __init__(self, state, transactionList, monthCode):
        QWidget.__init__(self)
        self.allTransactions = []
        self.state = state
        self.addListeners()
        self.loadNewMonth(transactionList, monthCode)

    def addListeners(self):
        self.state.addSubscriber(Events.transaction_drop_event, self.dropEvent)
        self.state.addSubscriber(Events.remove_category, self.removeCategory)
        self.state.addSubscriber(Events.update_category_total, self.updateConfigCategoryTotal)
        self.state.addSubscriber(Events.update_category_title, self.updateConfigCategoryName)
        self.state.addSubscriber(Events.add_category, self.addCategory)

    def onDestroy(self):
        self.state.removeSubscriber(Events.transaction_drop_event, self.dropEvent)
        self.state.removeSubscriber(Events.remove_category, self.removeCategory)
        self.state.removeSubscriber(Events.update_category_total, self.updateConfigCategoryTotal)
        self.state.removeSubscriber(Events.update_category_title, self.updateConfigCategoryName)
        self.state.removeSubscriber(Events.add_category, self.addCategory)

    def addCategory(self, data):
        cfg = self.state.getConfig()
        if not data['title'] in cfg['months'][self.month]:
            amt = int(data['amt'])
            cfg['months'][self.month][data['title']] = {
                'transactionList': [],
                'total': amt
            }
            self.state.setConfig(cfg)

            idx = -1
            if data['title'] == 'Income':
                idx = 0
            else:
                for i, section in enumerate(self.sectionState):
                    if int(section['total']) < amt:
                        idx = i
                        break

            self.sectionState.insert(idx, {'name': data['title'], 'total': amt})
            self.contentWrapperLayout.insertWidget(idx, Category(data['title'], amt, [], self.state))
            self.updateTotalAmt()

    def loadNewMonth(self, transactionList, monthCode, disableCredit=False):
        self.allTransactions = transactionList
        self.month = monthCode
        self.constructCategories(transactionList, monthCode)
        self.updateTotalAmt()

    def constructCategories(self, transactionList, monthCode):
        config = self.state.getConfig()
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
        incomeCategory = None
        for category in categoryKeys:
            if category == 'income' and formattedSections['income']['total'] > 0:
                self.sectionState.append({'name': 'Income', 'total': formattedSections['income']['total']})
                incomeCategory = {
                    'title': 'Income',
                    'amt': formattedSections['income']['total']
                }
            elif category == 'uncategorized':
                self.sectionState.append({'name': 'Uncategorized', 'total': '0'})
                sectionsUI.append(Category('Uncategorized', '0', formattedSections['uncategorized']['tList'], self.state))
            else:
                catTotal = config['months'][monthCode][category]['total']
                self.sectionState.append({'name': category, 'total': catTotal})
                sectionsUI.append(Category(category, catTotal, formattedSections[category]['tList'], self.state))

        self.contentWrapperLayout = QVBoxLayout()
        for sectionLayout in sectionsUI:
            self.contentWrapperLayout.addWidget(sectionLayout)
        self.setLayout(self.contentWrapperLayout)
        self.state.setConfig(config)
        if incomeCategory:
            self.addCategory(incomeCategory)
            incomeCategoryWidget = self.getCategoryWidget('Income')
            incomeCategoryWidget.addTransactions(formattedSections['income']['tList'])

    def updateConfigCategoryTotal(self, name, amt):
        cfg = self.state.getConfig()
        cfg['months'][self.month][name]['total'] = amt
        self.state.setConfig(cfg)
        self.updateTotalAmt()

    def updateConfigCategoryName(self, name, newTitle):
        cfg = self.state.getConfig()
        cfg['months'][self.month][newTitle] = cfg['months'][self.month].pop(name)
        self.state.setConfig(cfg)

    def dropEvent(self, transactionTitle, destCategoryTitle):
        cfg = self.state.getConfig()
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

            self.state.setConfig(cfg)
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
        cfg = self.state.getConfig()

        amt = cfg['months'][self.month][title]['total']
        del cfg['months'][self.month][title]

        self.state.setConfig(cfg)
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
        self.updateTotalAmt()


    def getTotalAmt(self):
        totalAmt = 0
        for transaction in self.allTransactions:
            totalAmt += (-1 * transaction.amt) if transaction.isCredit else transaction.amt
        return round(totalAmt, 2)

    def sumCategories(self):
        cfg = self.state.getConfig()
        sum = 0
        categories = list(cfg['months'][self.month].keys())
        for category in categories:
            categoryTotal = cfg['months'][self.month][category]['total']
            sum += categoryTotal if category != 'Income' else -categoryTotal
        return sum

    def updateTotalAmt(self):
        categorySum = self.sumCategories()
        transactionSum = self.getTotalAmt()
        self.state.next(Events.update_total, transactionSum, categorySum)