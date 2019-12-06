from utils import Transaction

class AnzHelper:
    @staticmethod
    def buildAnzList(data):
        transactions = []
        for idx, row in data.iterrows():
            name = AnzHelper.getAnzTransactionName(row)
            displayName = name if len(name) < 35 else (name[:32] + '...')
            if 'Processed Date' in row:
                timestamp = row['Processed Date']
                date = '{}-{}-{}'.format(timestamp.day, timestamp.month, timestamp.year)
            else:
                date = row['Date'].replace('/', '-')
            amount = row['Amount']
            credit = amount if amount > 0 else None
            debit = abs(amount) if amount <= 0 else None
            newTransaction = Transaction(displayName, debit, credit, date, name)
            transactions.append(newTransaction)
        return transactions

    @staticmethod
    def getAnzTransactionName(transactionRow):
        transactionType = transactionRow['Type']
        if transactionType == 'Direct Credit'\
                or transactionType == 'Eft-Pos' \
                or transactionType == 'Bank Fee' \
                or transactionType == 'Payment':
            return transactionType + ': ' + transactionRow['Details'] + ' ' + transactionRow['Reference']

        elif transactionType == 'Atm Debit'\
                or transactionType == 'Chq/Withdrawal':
            return transactionType + ' ' + transactionRow['Particulars']

        elif transactionType == 'Deposit'\
                or transactionType == 'Visa Purchase':
            return transactionType + ': ' + (transactionRow['Code'] or '')

        elif transactionType == 'Bill Payment':
            return 'Bill: {} {}'.format(transactionRow['Details'], transactionRow['Reference'] or transactionRow['Particulars'])

        else:
            return transactionType