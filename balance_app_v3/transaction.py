class Transaction:
    def __init__(self, transaction_type, amount, date, category, sub_category):
        self.id = None
        self.transaction_type = transaction_type
        self.amount = amount
        self.date = date
        self.category = category
        self.sub_category = sub_category

