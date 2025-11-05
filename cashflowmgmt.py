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

def add_cashflow(cashflow):
    print('Enter flow type (i)ncome/(e)xpense: ')
    while True:
        flow_type: str = getchit()
        match(flow_type):
            case 'i':
                flow_type = 'Income'
                break
            case 'e':
                flow_type = 'Expense'
                break
            case _:
                print('Please input "i" for Income OR "e" for Expense')
    while True:
        try:
            amount:float = float(input('Enter amount: '))
            if isinstance(amount, float) and amount > 0:
                if flow_type == 'Expense':
                    amount = -amount
                    break
                else:
                    break
        except ValueError:
            pass
        print('Invalid amount. Please enter a number.')

    while True:
        if flow_type == "Income":
            print('(1) Wages')
            print('(2) Capital Gains')
            print('(3) Government Assistance (SSI, TANF, GA)')
            print('(4) Other')
            category: str = getchit()
            match(category):
                case '1':
                    category = 'Wages'
                    break
                case '2':
                    category = 'Capital Gains'
                    break
                case '3':
                    category = 'Gov. Assist.'
                    break
                case '4':
                    category = 'Other'
                    break
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
                    category = 'Bills'
                    break
                case '2':
                    category = 'Grocery'
                    break
                case '3':
                    category = 'Subscription'
                    break
                case '4':
                    while True:
                        print("Is this a (m)inimum debt payment or (p)rincipal debt payment? ")
                        debt = getchit()
                        if debt == 'm':
                            category = 'Debt'
                            break
                        elif debt == 'p':
                            category = 'Debt Extra'
                            break
                        else:
                            print("Press m for minimum payment, p for principal")
                    break
                case '5':
                    category = 'Other - Monthly'
                    break
                case '6':
                    category = 'Other - Biweekly'
                case _:
                    print('Invalid Entry, please select from the provided categories.')
                    pass
            
    description: str = input('Enter description: ')

    while True:
        if flow_type == "Expense":
            try:
                if category == 'Grocery':
                    payperiod = "M"
                    break
                day = input('Enter day of month due (1-31): ')
                if (1 <= int(day) <= 31):
                    payperiod = find_pay_period(int(day))
                    break
                else:
                    print("Please enter a number between 1 & 31")
            except ValueError:
                    print('Invalid day. Please enter a number between 1 and 31.')
        else:
            payperiod = "I"
            break
    for each in cashflow.people:
        print(each)
    while True:
        payee: str = input('Select a Payee: ')
        if payee in cashflow.people:
            break
        else:
            print("Please enter a name from existing people.")
    cashflow.cashflows.append({'id': str(uuid.uuid4())[:4], 'category': category, 'description': description, 'amount': amount,  'payperiod': payperiod, 'payee': payee,'flow_type': flow_type})

def remove_cashflow(cashflow, id):
    for index, item in enumerate(cashflow.cashflows):
        if item['id'] == id:
            print(tabulate([cashflow.cashflows[index]], headers='keys'))
            print("Are you sure you want to remove? (y)es or (n)o")
            while True:
                confirmation = getchit()
                if confirmation == 'y':
                    cashflow.cashflows.pop(index)
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

def cashflow_management(cashflow):
        while True:
            clear_screen()
            print("Current Cashflows")
            print_cashflow(cashflow.cashflows)
            print("(a)dd or (r)emove cashflow?")
            print("Press b to go back")
            cfmgmt = getchit()
            match(cfmgmt):
                case 'a':
                    add_cashflow(cashflow)
                case 'r':
                    print_cashflow(cashflow.cashflows)
                    id = input('Enter the ID of cashflow to be removed: ')
                    remove_cashflow(cashflow, id)
                case 'b':
                    break