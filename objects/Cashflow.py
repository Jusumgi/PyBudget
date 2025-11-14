import uuid
from tools import getchit

class Cashflow:
    def __init__(self, expense_plan):
        self.id = str(uuid.uuid4())[:4]
        self.flow_type = determine_cashflow_type()
        if self.flow_type == 'Cancel':
            return
        self.amount = get_cashflow_amount(self.flow_type)
        self.category = determine_category(self.flow_type)
        self.description = input('Enter description: ')
        self.payperiod = pay_date_select(self.flow_type, self.category)
        self.payee = payee_select(expense_plan)

def find_pay_period(day, expense_plan):
    match expense_plan.payperiod_selector:
        case "Monthly":
            return "M"
        case "Weekly":
            if 1 <= day <= 7:
                return "D"
            elif 8 <= day <= 14:    
                return "C"
            elif 15 <= day <= 21:
                return "B"
            else:
                return "A"
        case "Biweekly":
            if 1 <= day <= 15 :
                return "B"
            else:
                return "A" 

def payee_select(expense_plan):
    for each in expense_plan.people:
        print(each)
    while True:
        payee: str = input('Select a Payee: ')
        if payee in expense_plan.people:
            return payee
        else:
            print("Please enter a name from existing people.")

def pay_date_select(flow_type, category):
    while True:
        if flow_type == "Expense":
            try:
                if category == 'Grocery' or category == 'Other - Monthly':
                    return "M"
                day = input('Enter day of month due (1-31): ')
                if (1 <= int(day) <= 31):
                    return find_pay_period(int(day))
                else:
                    print("Please enter a number between 1 & 31")
            except ValueError:
                    print('Invalid day. Please enter a number between 1 and 31.')
        else:
            return "I"
        
def determine_cashflow_type():
    print('Enter flow type (i)ncome/(e)xpense: ')
    print('(c) to cancel')
    while True:
        flow_type: str = getchit().lower()
        match(flow_type):
            case 'i':
                return 'Income'
            case 'e':
                return 'Expense'
            case 'c':
                return 'Cancel'
            case _:
                print('Please input "i" for Income OR "e" for Expense or "c" to cancel.')

def get_cashflow_amount(flow_type):
    while True:
        try:
            amount:float = float(input('Enter amount: '))
            if isinstance(amount, float) and amount > 0:
                if flow_type == 'Expense':
                    return -amount
                else:
                    return amount
        except ValueError:
            pass
        print('Invalid amount. Please enter a number.')

def determine_category(flow_type):
    while True:
        if flow_type == "Income":
            print('(1) Wages')
            print('(2) Capital Gains')
            print('(3) Government Assistance (SSI, TANF, GA)')
            print('(4) Other')
            category: str = getchit()
            match(category):
                case '1':
                    return'Wages'
                    
                case '2':
                    return 'Capital Gains'
                    
                case '3':
                    return 'Gov. Assist.'
                    
                case '4':
                    return 'Other'
                    
                case _:
                    print('Invalid Entry, please select from the provided categories.')
        else:
            print('(1) Bills')
            print('(2) Grocery')
            print('(3) Subscription')
            print('(4) Debt')
            print('(5) Other - Monthly')
            print('(6) Other - Biweekly')
            print("Select a category")
            category: str = getchit()
            match(category):
                case '1':
                    return 'Bills'
                case '2':
                    return 'Grocery'
                case '3':
                    return 'Subscription'
                case '4':
                    while True:
                        print("Is this a (m)inimum debt payment or (p)rincipal debt payment? ")
                        debt = getchit().lower()
                        if debt == 'm':
                            return 'Debt'
    
                        elif debt == 'p':
                            return 'Debt Extra'
    
                        else:
                            print("Press m for minimum payment, p for principal")
                case '5':
                    return 'Other - Monthly'
                case '6':
                    return 'Other - Biweekly'
                case _:
                    print('Invalid Entry, please select from the provided categories.')
                    pass