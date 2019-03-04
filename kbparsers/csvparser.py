from datetime import date
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

    def formatDate(self, dateStr):
        day, month, year = dateStr.split('-')
        transactionDate = date(int(year), int(month), int(day))
        print(str(transactionDate.month))
        return transactionDate

    def buildFullList(self, lines):
        transactions = []
        for line in lines:
            values = line.split(',')
            if re.search(self.dateMatch, values[self.dateIdx]):
                description = self.formatDescription(values[self.descriptionIdx])
                amountDebit = values[self.amountDebitIdx]
                date = self.formatDate(values[self.dateIdx])
                amountCredit = values[self.amountCreditIdx]
                newTransaction = Transaction(description, amountDebit, amountCredit, date)
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
