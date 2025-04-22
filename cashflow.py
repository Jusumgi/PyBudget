from colorama import Fore, Style
from tabulate import tabulate
import getch
import uuid
import os
import platform
import copy
import ast
import getfiles


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
        peepmgmt = getch.getch()
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
def clear_screen():
    system = platform.system()
    if system == "Windows":
        os.system('cls')
    elif system == "Linux" or system == "Darwin":
        os.system('clear')
    else:
        print("Operating System not supported")

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
                break
        except ValueError:
            pass
        print('Invalid amount. Please enter a number.')

    while True:
        if flow_type == "Income":
            category = "Income"
            break
        else:
            print('(1) Bills')
            print('(2) Grocery')
            print('(3) Subscription')
            print('(4) Debt')
            print('(5) Misc')
            print("Select a category")
            category = getch.getch()
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
        try:
            day = input('Enter day of month due (1-31): ')
            if (1 <= int(day) <= 31):
                break
            else:
                print("Please enter a number between 1 & 31")
        except ValueError:
                print('Invalid day. Please enter a number between 1 and 31.')
    for each in cashflow['people']:
        print(each)
    while True:
        payee = input('Select a Payee: ')
        if payee in cashflow['people']:
            break
        else:
            print("Please enter a name from existing people.")
    cashflow['cashflows'].append({'id': str(uuid.uuid4())[:4], 'category': category, 'description': description, 'amount': amount,  'day': day, 'payee': payee,'flow_type': flow_type})

def remove_cashflow(cashflow, id):
    for index, item in enumerate(cashflow['cashflows']):
        if item['id'] == id:
            print(tabulate([cashflow['cashflows'][index]], headers='keys'))
            print("Are you sure you want to remove? (y)es or (n)o")
            while True:
                confirmation = getch.getch()
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
            cfmgmt = getch.getch()
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
    try:
        return sum(map(lambda cf: cf['amount'], cashflow['cashflows']))
    except TypeError:
        print("Broken :(")
        getch.getch()
        
    
def filter_cashflow_by_id(cashflow, id):
    return filter(lambda expense: expense['id'] == id, cashflow)
    

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
        choice = getch.getch()

        match(choice):
            case '1':
                while True:
                    if not cashflow['people']:
                        print("Please add people first.")
                        getch.getch()
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
                print('\nTotal cashflow: ', total_cashflow(cashflow))
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
