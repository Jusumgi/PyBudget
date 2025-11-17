class Engine:
    """
    The main engine that runs the budgeting application.
    It manages people and their associated expense plans.
    """
    def __init__(self):
        self.people = []
        self.expense_plans = []
        self.current_expense_plan = None