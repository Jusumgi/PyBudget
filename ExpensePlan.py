from tools import clear_screen, getchit, get_file_names
import ast
import copy
import tabulate
import pickle
from cashflowmgmt import *
from colorama import Fore, Style

class ExpensePlan:
    def __init__(self, filename):
        self.filename = filename
        self.cashflows = []
        self.people = []

    def add_people(self):
        while True:
            person_add = input("Enter a name to be added: ")
            if person_add:
                self.people.append(person_add)
                break
            else:
                print("Cannot enter a blank name.")

    def remove_people(self):
        person_remove = input("Enter a name to be removed: ")
        try:
            index = self.people.index(person_remove)
            self.people.pop(index)
        except ValueError:
            print("Name not found")

    def people_management(self, people):
        while True:
            clear_screen()
            print("Current People")
            for each in people:
                print(each)
            print("(a)dd or (r)emove people?")
            print("Press b to go back")
            peepmgmt = getchit()
            match(peepmgmt):
                case 'a':
                    self.add_people()  
                case 'r':
                    if len(self.people) == 0:
                        print("No people added")
                        input("Press any key to continue.")
                    else:
                        self.remove_people()
                case 'b':
                    break

    def print_cashflow(self):
        printed_cashflow = copy.deepcopy(self.cashflows)
        for each in printed_cashflow:
            if each['flow_type'] == 'Income':
                each['amount'] = Fore.GREEN + '$' + str(each['amount']) + Style.RESET_ALL
            else:
                each['amount'] = Fore.RED + '$' + str(each['amount']) + Style.RESET_ALL
        print(tabulate(printed_cashflow, headers='keys', disable_numparse=True, tablefmt='double_grid'))

    def total_cashflow(self, cashflow):
        
        # Initialize dictionaries to store totals and track categories per flow_type
        totals = {}
        categories_by_flow = {'Income': set(), 'Expense': set()}
        
        # Calculate totals and group categories by flow_type
        for each in self.cashflows:
            flow_type = each['flow_type']
            category = each['category']
            amount = round(each['amount'], 2)
            totals[flow_type] = totals.get(flow_type, 0) + amount
            totals[category] = totals.get(category, 0) + amount
            categories_by_flow[flow_type].add(category)

        income = round(totals['Income'], 2)
        expense = round(totals['Expense'], 2)
        # Calculate Disposable income (Income - Expense)
        disposable = round(income + expense, 2)

        def format_value(value):
            return (
                Fore.RED + '$' + str(value) + Style.RESET_ALL if value < 0
                else Fore.GREEN + '$' + str(value) + Style.RESET_ALL
            )
        # Format Disposable with color
        disposable_formatted = (
            Fore.RED + '$' + str(disposable) + Style.RESET_ALL if disposable < 0
            else Fore.GREEN + '$' + str(disposable) + Style.RESET_ALL
        )
        # Create separate dictionaries for Income, Expense, and Disposable rows
        income_row = {'Type': 'Income'}
        expense_row = {'Type': 'Expense'}
        disposable_row = {'Type': 'Disposable'}
        
        # Add Income and its categories to income_row
        if 'Income' in totals:
            income_row['Total'] = format_value(round(totals['Income'],2))
            for category in sorted(categories_by_flow['Income']):
                if category in totals:
                    income_row[category] = format_value(round(totals[category],2))
        
        # Add Expense and its categories to expense_row
        if 'Expense' in totals:
            expense_row['Total'] = format_value(round(totals['Expense'],2))
            for category in sorted(categories_by_flow['Expense']):
                if category in totals:
                    expense_row[category] = format_value(round(totals[category],2))
        # Add Disposable to disposable_row
        disposable_row['Total'] = disposable_formatted
        
        # Collect rows for tabulate (only include non-empty rows for Income and Expense)
        rows = []
        if len(income_row) > 1:  # Check if income_row has more than just 'Type'
            rows.append(income_row)
        if len(expense_row) > 1:  # Check if expense_row has more than just 'Type'
            rows.append(expense_row)
        rows.append(disposable_row)  # Always include Disposable row
        
        # Print the table using tabulate
        if rows:
            print(tabulate(rows, headers='keys', tablefmt='double_grid'))
        else:
            print("No data to display.")

    def cashflow_management(self, cashflow):
        while True:
            clear_screen()
            print("Current Cashflows")
            self.print_cashflow()
            print("(a)dd or (r)emove cashflow?")
            print("Press b to go back")
            cfmgmt = getchit()
            match(cfmgmt):
                case 'a':
                    add_cashflow(cashflow)
                case 'r':
                    self.print_cashflow()
                    id = input('Enter the ID of cashflow to be removed: ')
                    remove_cashflow(cashflow, id)
                case 'b':
                    break
            
    def display_expense_plan_menu(self):
        while True:
            clear_screen()
            print('Edit Expense Plan Menu')
            print("===========================")
            print('(1) Cashflow Management')
            print('(2) People Management')
            print('(3) List cashflow')
            print('(4) Show total cashflow')
            print('(q) Exit')
            print('--------------------------------')
            print('Select an option')
            choice = getchit()

            match(choice):
                case '1':
                    while True:
                        if not self.people:
                            print("Please add people first.")
                            getchit()
                            break
                        else:
                            self.cashflow_management(self)
                            break 
                case '2':
                    self.people_management(self.people)
                case '3':
                    clear_screen()
                    print('\nAll cashflow:')
                    self.print_cashflow()
                    input("Press any key to continue")
                case '4':
                    clear_screen()
                    # print('\nTotal cashflow: ', total_cashflow(cashflow))
                    self.total_cashflow(self.cashflows)
                    input("Press any key to continue")
                case 'q':
                    try:
                        return self
                    except UnboundLocalError:
                        print("Return failed")
                        break
