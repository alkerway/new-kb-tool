import re

from kbutils import Transaction

class CSVParser():
    def __init__(self):
        super(CSVParser, self).__init__()
        self.dateMatch = '[0-9].+-[0-9].+-.+'

    def formatDescription(self, description):
        name = description[:-2]
        if re.search('POS W/D .+', description):
            name = description[8:21] + '...'

        # if name in self.transactionNameMap:
        #     name = self.transactionNameMap[name]
        return name

    def separateByMonth(self, transactionList):
        transactionMap = {}
        for transaction in transactionList:
            yearMonth = str(transaction.date.year) + '-' + ('0' + str(transaction.date.month))[-2:]
            if yearMonth in transactionMap:
                transactionMap[yearMonth].append(transaction)
            else:
                transactionMap[yearMonth] = [transaction]

        return transactionMap

    def buildFullList(self, lines):
        transactions = []
        for line in lines:
            values = line.split(',')
            if re.search(self.dateMatch, values[self.dateIdx]):
                description = self.formatDescription(values[self.descriptionIdx])
                amountDebit = values[self.amountDebitIdx]
                date = values[self.dateIdx]
                amountCredit = values[self.amountCreditIdx]
                newTransaction = Transaction(description, amountDebit, amountCredit, date)
                if not newTransaction.isCredit or 'DOROSTK' not in newTransaction.name and 'LIVING EXPENSES' not in newTransaction.name:
                    transactions.append(newTransaction)

        return transactions


    def parseCsv(self, csvFileName):
        with open(csvFileName, 'r') as contents:
            lines = contents.read().splitlines()
            titles = lines[0].split(',')
            self.amountDebitIdx = titles.index('Amount (debit)')
            self.amountCreditIdx = titles.index('Amount (credit)')
            self.dateIdx = titles.index('Date')
            self.descriptionIdx = titles.index('Memo/Description')
            allTransactions = self.buildFullList(lines[1:])
            sortedTransactionsMap = self.separateByMonth(allTransactions)
            return sortedTransactionsMap

