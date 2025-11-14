from tools import getchit, clear_screen
from tabulate import tabulate
from colorama import Fore, Style
import copy
import uuid

def find_pay_period(day):
    if 1 <= day <= 15 :
        return "B"
    else:
        return "A" 
    
def save_cashflow(cashflow):
    savefile = input("Enter save name: ")
    with open("saves/"+savefile+".txt", "w") as file:
        file.write(str(cashflow))

def load_cashflow(filename):
    try:
        with open("saves/"+filename+".txt") as file:
            return file.read()
    except FileNotFoundError:
        return 5

def add_cashflow(expense_plan):
    flow_type:str = determine_cashflow_type()
    amount: float = get_cashflow_amount(flow_type)
    category:str = determine_category(flow_type)
    description: str = input('Enter description: ')
    payperiod = pay_date_select(flow_type, category)
    payee = payee_select(expense_plan)
    expense_plan.cashflows.append({'id': str(uuid.uuid4())[:4], 'category': category, 'description': description, 'amount': amount,  'payperiod': payperiod, 'payee': payee,'flow_type': flow_type})

def remove_cashflow(expense_plan, id):
    for index, item in enumerate(expense_plan.cashflows):
        if item['id'] == id:
            print(tabulate([expense_plan.cashflows[index]], headers='keys'))
            print("Are you sure you want to remove? (y)es or (n)o")
            while True:
                confirmation = getchit()
                if confirmation == 'y':
                    expense_plan.cashflows.pop(index)
                    print('Cashflow removed')
                    input("Press any key to continue")
                    break
                elif confirmation == 'n' :
                    print('Cashflow not removed.')
                    input("Press any key to continue")
                    break
                else:
                    print("Please press y or n")
    return -1



def print_cashflow(cashflow):
    printed_cashflow = copy.deepcopy(cashflow)
    for each in printed_cashflow:
        if each['flow_type'] == 'Income':
            each['amount'] = Fore.GREEN + '$' + str(each['amount']) + Style.RESET_ALL
        else:
            each['amount'] = Fore.RED + '$' + str(each['amount']) + Style.RESET_ALL
    print(tabulate(printed_cashflow, headers='keys', disable_numparse=True, tablefmt='double_grid'))

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
                if category == 'Grocery':
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
    while True:
        flow_type: str = getchit().lower()
        match(flow_type):
            case 'i':
                return 'Income'
            case 'e':
                return 'Expense'
            case _:
                print('Please input "i" for Income OR "e" for Expense')

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
                    pass
            break
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