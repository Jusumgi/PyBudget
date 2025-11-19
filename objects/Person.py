from objects.Cashflow import Cashflow
from tools import *
from colorama import Fore, Style
from tabulate import tabulate
import copy

class Person:
    """ Represents a person involved in an expense plan. """
    def __init__(self, name: str):
        self.name = name
        self.currency_symbol = currency_symbol_selection()
        self.cashflows = []
        self.associated_expense_plans = []

    def change_currency_symbol(self):
        """ Changes the currency symbol for the person. """
        new_symbol = currency_symbol_selection()
        self.currency_symbol = new_symbol
        print(f"Currency symbol for {self.name} updated to: {new_symbol}")
        input("Press any key to continue.")
        
    def cashflow_management(self):
        """ Manages adding and removing cashflows in the expense plan. """
        while True:
            clear_screen()
            print("Current Cashflows")
            self.print_cashflow()
            print("(a)dd or (r)emove cashflow?")
            print("Press b to go back")
            cfmgmt = getchit()
            match(cfmgmt):
                case 'a':
                    added_cashflow = Cashflow(self.name)
                    if added_cashflow.flow_type == 'Cancel':
                        print("Cashflow addition cancelled.")
                        input("Press any key to continue")
                    else:
                        self.cashflows.append(added_cashflow)
                case 'r':
                    self.print_cashflow()
                    self.remove_cashflow()
                case 'b':
                    break

    def remove_cashflow(self):
        """ Removes a cashflow from the expense plan by its ID. """
        id = input('Enter the ID of cashflow to be removed: ')
        found = False
        for index, item in enumerate(self.cashflows):
            each = item.__dict__ # Convert each Cashflow object to dict
            if each['id'] == id:
                found = True
                print(tabulate([each], headers='keys'))
                print("Are you sure you want to remove? (y)es or (n)o")
                while True:
                    confirmation = getchit()
                    if confirmation == 'y':
                        self.cashflows.pop(index)
                        print('Cashflow removed')
                        input("Press any key to continue")
                        break
                    elif confirmation == 'n' :
                        print('Cashflow not removed.')
                        input("Press any key to continue")
                        break
                    else:
                        print("Please press y or n")
                break        
        if not found:
            print(f"Cashflow with ID '{id}' not found.")
            input("Press any key to continue")

    def total_cashflow(self):
        """ Displays the total cashflow summary including income, expenses, and disposable income. """
        clear_screen()
        buffer = copy.deepcopy(self.cashflows)
        # Initialize dictionaries to store totals and track categories per flow_type
        totals = {}
        categories_by_flow = {'Income': set(), 'Expense': set()}
        
        # Calculate totals and group categories by flow_type
        for cashflow_obj in buffer:
            each = cashflow_obj.__dict__ # Convert each Cashflow object to dict
            flow_type = each['flow_type']
            category = each['category']
            amount = round(each['amount'], 2)
            totals[flow_type] = totals.get(flow_type, 0) + amount
            totals[category] = totals.get(category, 0) + amount
            categories_by_flow[flow_type].add(category)
        
        try: income = round(totals['Income'], 2)
        except KeyError: income = 0.0
        try: expense = round(totals['Expense'], 2)
        except KeyError: expense = 0.0
        # Calculate Disposable income (Income - Expense)
        disposable = round(income + expense, 2)

        def format_value(value):
            return (
                Fore.RED + self.currency_symbol + str(value) + Style.RESET_ALL if value < 0
                else Fore.GREEN + self.currency_symbol + str(value) + Style.RESET_ALL
            )
        # Format Disposable with color
        disposable_formatted = (
            Fore.RED + self.currency_symbol + str(disposable) + Style.RESET_ALL if disposable < 0
            else Fore.GREEN + self.currency_symbol + str(disposable) + Style.RESET_ALL
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

    def print_cashflow(self):
        """ Prints the cashflows in a tabulated format with color coding for income and expenses. """
        clear_screen()
        buffer:list[object] = copy.deepcopy(self.cashflows)
        printed_cashflow = []
        for cashflow_obj in buffer: # Convert each Cashflow object to dict
            each: dict = cashflow_obj.__dict__
            if each['flow_type'] == 'Income':
                each['amount'] = Fore.GREEN + self.currency_symbol + str(each['amount']) + Style.RESET_ALL
            else:
                each['amount'] = Fore.RED + self.currency_symbol + str(each['amount']) + Style.RESET_ALL
            printed_cashflow.append(each)
        print(tabulate(printed_cashflow, headers='keys', disable_numparse=True, tablefmt='double_grid'))