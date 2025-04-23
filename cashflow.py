from colorama import Fore, Style
from tabulate import tabulate
from getch import getch
import uuid
from clearscreen import clear_screen
import copy
import ast
import getfiles

def find_pay_period(day):
    if 1 <= day <= 15 :
        return "B"
    else:
        return "A" 
    
def add_people(cashflow):
    while True:
        person_add = input("Enter a name to be added: ")
        if person_add:
            cashflow['people'].append(person_add)
            break
        else:
            print("Cannot enter a blank name.")

def remove_people(cashflow):
    person_remove = input("Enter a name to be removed: ")
    try:
        index = cashflow['people'].index(person_remove)
        cashflow['people'].pop(index)
    except ValueError:
        print("Name not found")

def people_management(cashflow):
    while True:
        clear_screen()
        print("Current People")
        for each in cashflow['people']:
            print(each)
        print("(a)dd or (r)emove people?")
        print("Press b to go back")
        peepmgmt = getch()
        match(peepmgmt):
            case 'a':
                add_people(cashflow)  
            case 'r':
                if len(cashflow['people']) == 0:
                    print("No people added")
                    input("Press any key to continue.")
                else:
                    remove_people(cashflow)
            case 'b':
                break


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
        flow_type = getch.getch()
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
            amount = float(input('Enter amount: '))
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
            category = getch.getch()
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
            print('(5) Misc')
            print("Select a category")
            category = getch()
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
                    category = 'Debt'
                    break
                case '5':
                    category = 'Misc'
                    break
                case _:
                    print('Invalid Entry, please select from the provided categories.')
                    pass
            
    description = input('Enter description: ')

    while True:
        if flow_type == "Expense":
            try:
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
    for each in cashflow['people']:
        print(each)
    while True:
        payee = input('Select a Payee: ')
        if payee in cashflow['people']:
            break
        else:
            print("Please enter a name from existing people.")
    cashflow['cashflows'].append({'id': str(uuid.uuid4())[:4], 'category': category, 'description': description, 'amount': amount,  'payperiod': payperiod, 'payee': payee,'flow_type': flow_type})

def remove_cashflow(cashflow, id):
    for index, item in enumerate(cashflow['cashflows']):
        if item['id'] == id:
            print(tabulate([cashflow['cashflows'][index]], headers='keys'))
            print("Are you sure you want to remove? (y)es or (n)o")
            while True:
                confirmation = getch()
                if confirmation == 'y':
                    cashflow['cashflows'].pop(index)
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

def cashflow_management(cashflow):
        while True:
            clear_screen()
            print("Current Cashflows")
            print_cashflow(cashflow)
            print("(a)dd or (r)emove cashflow?")
            print("Press b to go back")
            cfmgmt = getch()
            match(cfmgmt):
                case 'a':
                    add_cashflow(cashflow)
                case 'r':
                    print_cashflow(cashflow)
                    id = input('Enter the ID of cashflow to be removed: ')
                    remove_cashflow(cashflow, id)
                case 'b':
                    break
def print_cashflow(cashflow):
    printed_cashflow = copy.deepcopy(cashflow)
    for each in printed_cashflow['cashflows']:
        if each['flow_type'] == 'Income':
            each['amount'] = Fore.GREEN + '$' + str(each['amount']) + Style.RESET_ALL
        else:
            each['amount'] = Fore.RED + '$' + str(each['amount']) + Style.RESET_ALL
    print(tabulate(printed_cashflow['cashflows'], headers='keys', disable_numparse=True, tablefmt='double_grid'))

def total_cashflow(cashflow):
    # Initialize dictionaries to store totals and track categories per flow_type
    totals = {}
    categories_by_flow = {'Income': set(), 'Expense': set()}
    
    # Calculate totals and group categories by flow_type
    for each in cashflow['cashflows']:
        flow_type = each['flow_type']
        category = each['category']
        amount = each['amount']
        totals[flow_type] = totals.get(flow_type, 0) + amount
        totals[category] = totals.get(category, 0) + amount
        categories_by_flow[flow_type].add(category)
    
    # Format totals with color based on value
    for key in totals:
        if totals[key] < 0:
            totals[key] = Fore.RED + '$' + str(totals[key]) + Style.RESET_ALL
        else:
            totals[key] = Fore.GREEN + '$' + str(totals[key]) + Style.RESET_ALL
    
    # Create separate dictionaries for Income and Expense rows
    income_row = {'Type': 'Income'}
    expense_row = {'Type': 'Expense'}
    
    # Add Income and its categories to income_row
    if 'Income' in totals:
        income_row['Total'] = totals['Income']
        for category in sorted(categories_by_flow['Income']):
            if category in totals:
                income_row[category] = totals[category]
    
    # Add Expense and its categories to expense_row
    if 'Expense' in totals:
        expense_row['Total'] = totals['Expense']
        for category in sorted(categories_by_flow['Expense']):
            if category in totals:
                expense_row[category] = totals[category]
    
    # Collect rows for tabulate (only include non-empty rows)
    rows = []
    if len(income_row) > 1:  # Check if income_row has more than just 'Type'
        rows.append(income_row)
    if len(expense_row) > 1:  # Check if expense_row has more than just 'Type'
        rows.append(expense_row)
    
    # Print the table using tabulate
    if rows:
        print(tabulate(rows, headers='keys', tablefmt='double_grid'))
    else:
        print("No data to display.")

def cashflowed(filename, loaded_cashflow):
    cashflow = {"filename": filename, "cashflows":loaded_cashflow['cashflows'], "people": loaded_cashflow['people']}
    try:
        with open("saves/people.txt") as file:
                people = ast.literal_eval(file.read())
                print(people)
    except FileNotFoundError:
        pass
    while True:
        clear_screen()
        print('\nExpense Tracker')
        print('(1) Cashflow Management')
        print('(2) People Management')
        print('(3) List cashflow')
        print('(4) Show total cashflow')
        print('(5) Save Cashflow')
        print('(6) Load Cashflow')
        print('(q) Exit')
        print('--------------------------------')
        print('Select an option')
        choice = getch()

        match(choice):
            case '1':
                while True:
                    if not cashflow['people']:
                        print("Please add people first.")
                        getch()
                        break
                    else:
                        cashflow_management(cashflow)
                        break 
            case '2':
                people_management(cashflow)
            case '3':
                clear_screen()
                print('\nAll cashflow:')
                print_cashflow(cashflow)
                input("Press any key to continue")
            case '4':
                clear_screen()
                # print('\nTotal cashflow: ', total_cashflow(cashflow))
                total_cashflow(cashflow)
                input("Press any key to continue")
            case '5':
                save_cashflow(cashflow)
            case '6':
                clear_screen()
                print(getfiles.get_file_names("saves/"))
                cashflow_filename = input("Enter file name: ")
                loaded_file = load_cashflow(cashflow_filename)
                if loaded_file == 5:
                    clear_screen()
                    print("File was not found.")
                    input('Press any key to continue')
                else:
                    cashflow = ast.literal_eval(loaded_file)
                    clear_screen()
                    print_cashflow(cashflow)
                    input('Press any key to continue')
            case 'q':
                try:
                    return cashflow
                except UnboundLocalError:
                    print("Return failed")
                    break
