import pandas as pd

from .kiwibankhelper import KiwibankHelper
from .anzhelper import AnzHelper

class CSVParser():
    def __init__(self):
        super(CSVParser, self).__init__()

    def separateByMonth(self, transactionList):
        transactionMap = {}
        for transaction in transactionList:
            yearMonth = str(transaction.date.year) + '-' + ('0' + str(transaction.date.month))[-2:]
            if yearMonth in transactionMap:
                transactionMap[yearMonth].append(transaction)
            else:
                transactionMap[yearMonth] = [transaction]

        return transactionMap

    def parseCsv(self, csvFileName):
        data = pd.read_excel(csvFileName, keep_default_na=False) if '.xlsx' in csvFileName else pd.read_csv(csvFileName, keep_default_na=False)
        allTransactions = []
        if 'Amount (debit)' in data.columns:
            allTransactions = KiwibankHelper.buildKiwibankList(data)
        elif 'Foreign Currency Amount' in data.columns or 'ForeignCurrencyAmount' in data.columns:
            allTransactions = AnzHelper.buildAnzList(data)
        else:
            print('Unrecognized statement')
            return {}
        sortedTransactionsMap = self.separateByMonth(allTransactions)
        return sortedTransactionsMap

    def addTransactionMap(self, oldTransactionMap, newTransactionMap):
        for month in newTransactionMap.keys():
            if month in oldTransactionMap:
                oldTransactionMap[month] += newTransactionMap[month]
                oldTransactionMap[month].sort(key=lambda t: t.date)
            else:
                oldTransactionMap[month] = newTransactionMap[month]
        return oldTransactionMap

