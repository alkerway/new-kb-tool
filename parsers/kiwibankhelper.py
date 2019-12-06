from utils import Transaction
import re


class KiwibankHelper:
    @staticmethod
    def buildKiwibankList(data):
        dateMatch = '[0-9].+-[0-9].+-.+'

        transactions = []
        for idx, row in data.iterrows():
            if re.search(dateMatch, row['Date']):
                description = row['Memo/Description']
                displayName = KiwibankHelper.formatDescription(description)
                date = row['Date']
                debit = row['Amount (debit)'] or None
                credit = row['Amount (credit)'] or None
                newTransaction = Transaction(displayName, debit, credit, date, description)
                transactions.append(newTransaction)
        return transactions

    @staticmethod
    def formatDescription(description):
        name = description[:-2]
        if re.search('POS W/D .+', description):
            name = description[8:21] + '...'

        # if name in self.transactionNameMap:
        #     name = self.transactionNameMap[name]
        return name[:35]