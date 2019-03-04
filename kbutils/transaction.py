class Transaction:
    def __init__(self, name, amtDebit, amtCredit, date):
        self.name = name
        self.amt = amtDebit or amtCredit
        self.date = date
        self.isCredit = not amtDebit
