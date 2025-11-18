class Person:
    """ Represents a person involved in an expense plan. """
    def __init__(self, name: str):
        self.name = name
        self.cashflows = []
        self.expense_plans = []