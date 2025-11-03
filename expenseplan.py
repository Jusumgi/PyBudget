class ExpensePlan:
    def __init__(self, filename, loaded_cashflow):
        self.filename = filename
        self.cashflows = loaded_cashflow['cashflows']
        self.people = loaded_cashflow['people']