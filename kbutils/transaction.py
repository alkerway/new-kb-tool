from datetime import date

class Transaction:
    def __init__(self, displayName, amtDebit, amtCredit, date, description):
        self.name = description
        self.displayName = displayName
        amt = amtDebit or amtCredit
        self.amt = float(amt)
        self.date = self.formatDate(date)
        self.isCredit = not amtDebit

    def formatDate(self, dateStr):
        day, month, year = dateStr.split('-')
        transactionDate = date(int(year), int(month), int(day))
        return transactionDate
