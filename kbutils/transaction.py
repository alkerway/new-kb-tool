from datetime import date

class Transaction:
    def __init__(self, name, amtDebit, amtCredit, date):
        self.name = name
        amt = amtDebit or amtCredit
        self.amt = float(amt)
        self.date = self.formatDate(date)
        self.isCredit = not amtDebit

    def formatDate(self, dateStr):
        day, month, year = dateStr.split('-')
        transactionDate = date(int(year), int(month), int(day))
        return transactionDate
