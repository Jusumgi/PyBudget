from tools import clear_screen, getchit
import copy
from tabulate import tabulate
from colorama import Fore, Style
from objects.Cashflow import Cashflow
from objects.Person import Person

class ExpensePlan:
    """ Represents an expense plan with cashflows and people involved. """
    def __init__(self, filename, people: list[Person]):
        self.filename: str = filename
        self.payperiod_selector: str = 'Biweekly'
        self.people:list[Person] = people
        self.cashflows: list[dict] = self.accumulate_cashflows()

    def set_pay_period():
        print('Set pay period for Expense Plan:')
        print('(1) for Weekly')
        print('(2) for Biweekly (Default)')
        print('(3) for Monthly')
        while True:
            payperiod: str = getchit().lower()
            match(payperiod):
                case '1':
                    return 'Weekly'
                case '2':
                    return 'Biweekly'
                case '3':
                    return 'Monthly'
                case _:
                    print('Please input "1", "2", or "3" to select pay period.')

    def find_pay_period(self, day): #may not be needed in this object, but here for now
        """ Determines the pay period code based on the day and expense plan's pay period selector. """
        if day == "I":
            return "I"
        match self.payperiod_selector:
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
    def add_people(self):
        """ Adds a person from file to the expense plan by name. """
        while True:
            person_add: str = input("Enter a name to be added: ")
            if person_add:
                self.people.append(Person(person_add))
                break
            else:
                print("Cannot enter a blank name.")

    def remove_people(self):
        """ Removes a person from program by name. """
        name = input('Enter the name of cashflow to be removed: ')
        found = False
        for index, item in enumerate(self.people):
            each = item.__dict__ # Convert each Person object to dict
            if each['name'] == name:
                found = True
                print(each)
                print("Are you sure you want to remove? (y)es or (n)o")
                while True:
                    confirmation = getchit()
                    if confirmation == 'y':
                        self.cashflows.pop(index)
                        print('Person removed')
                        input("Press any key to continue")
                        break
                    elif confirmation == 'n' :
                        print('Person not removed.')
                        input("Press any key to continue")
                        break
                    else:
                        print("Please press y or n")
                break        
        if not found:
            print(f"Person with name '{name}' not found.")
            input("Press any key to continue")

    def people_management(self, people: list):
        """ Manages adding and removing people from the expense plan. """
        while True:
            clear_screen()
            print("Current People")
            for each in people:
                each = each.__dict__
                print(each['name'])
            print("(a)dd or (r)emove people?")
            print("Press b to go back")
            peepmgmt = getchit()
            match(peepmgmt):
                case 'a':
                    self.add_people()  
                case 'r':
                    if len(self.people) == 0:
                        print("No people to remove.")
                        input("Press any key to continue.")
                    else:
                        self.remove_people()
                case 'b':
                    break

    def print_cashflow(self):
        """ Prints the cashflows in a tabulated format with color coding for income and expenses. """
        clear_screen()
        buffer:list[object] = copy.deepcopy(self.cashflows)
        printed_cashflow = []
        for cashflow_obj in buffer: # Convert each Cashflow object to dict
            each: dict = cashflow_obj.__dict__
            if each['flow_type'] == 'Income':
                each['amount'] = Fore.GREEN + '$' + str(each['amount']) + Style.RESET_ALL
            else:
                each['amount'] = Fore.RED + '$' + str(each['amount']) + Style.RESET_ALL
            printed_cashflow.append(each)
        print(tabulate(printed_cashflow, headers='keys', disable_numparse=True, tablefmt='double_grid'))

    def print_expenseplan(self):
        """ Prints a summary of the expense plan including totals by type and payee assignments. """
        clear_screen()
        buffer:list[dict] = copy.deepcopy(self.cashflows)
        # Initialize dictionaries to store totals and track payperiods per flow_type
        totals = {}
        payperiods_by_flow = {'Income': set(), 'Expense': set()}
        payee_totals = {}
        payee_income = {}
        
        # Calculate totals and group payperiods by flow_type
        for cashflow_obj in buffer:
            each = cashflow_obj.__dict__ # Convert each Cashflow object to dict
            flow_type = each['flow_type']
            payperiod = self.find_pay_period(each['payperiod'])
            amount = each['amount']
            payee = each['payee']
            
            # Update flow_type and payperiod totals
            totals[flow_type] = totals.get(flow_type, 0) + amount
            totals[payperiod] = totals.get(payperiod, 0) + amount
            payperiods_by_flow[flow_type].add(payperiod)
            
            # Update payee income for Income transactions
            if flow_type == 'Income':
                payee_income[payee] = payee_income.get(payee, 0) + amount
            
            # Update payee totals for Expenses only
            if flow_type == 'Expense':
                if payee not in payee_totals:
                    payee_totals[payee] = {'total': 0, 'M': 0, 'A': 0, 'B': 0}
                payee_totals[payee]['total'] += amount
                payee_totals[payee][payperiod] += amount
        
        # Round totals for calculations
        income = round(totals.get('Income', 0), 2)
        half_income = round(totals.get('I', 0), 2) / 2
        expense = round(totals.get('Expense', 0), 2)
        monthly = round(totals.get('M', 0), 2)
        a_expense = round(totals.get('A', 0), 2)
        b_expense = round(totals.get('B', 0), 2)
        
        # Calculate Disposable income (Income - Expense)
        disposable = round(income + expense, 2)
        
        # Helper function to format values with color
        def format_value(value):
            return (
                Fore.RED + '$' + str(value) + Style.RESET_ALL if value < 0
                else Fore.GREEN + '$' + str(value) + Style.RESET_ALL
            )
        
        # Create separate dictionaries for Income, Expense, Disposable, and Disp. Split rows
        income_row = {'Type': 'Income', 'Total': format_value(income)}
        expense_row = {'Type': 'Expense', 'Total': format_value(expense)}
        disposable_row = {'Type': 'Disposable', 'Total': format_value(disposable)}
        each_row = {'Type': 'Disp. Split'}
        
        # Expense: Split payperiod M evenly between A and B, add direct A and B expenses
        expense_a = monthly / 2 + a_expense
        expense_b = monthly / 2 + b_expense
        
        # Disposable: Difference between Income and Expense for A and B
        disposable_a = round(half_income + expense_a, 2)
        disposable_b = round(half_income + expense_b, 2)
        
        # Split disposable by number of people
        people = self.people
        split_disposable_a = disposable_a / len(people) if people else disposable_a
        split_disposable_b = disposable_b / len(people) if people else disposable_b
        
        # Add formatted A and B values to rows
        income_row['A'] = format_value(half_income)
        income_row['B'] = format_value(half_income)
        expense_row['A'] = format_value(round(expense_a,2))
        expense_row['B'] = format_value(round(expense_b,2))
        disposable_row['A'] = format_value(disposable_a)
        disposable_row['B'] = format_value(disposable_b)
        each_row['A'] = format_value(round(split_disposable_a, 2))
        each_row['B'] = format_value(round(split_disposable_b, 2))
        
        # Collect rows for Type table
        rows = [income_row, expense_row, disposable_row, each_row]
        
        # Print the Type table
        print("Cashflow by Type:")
        print(tabulate(rows, headers='keys', tablefmt='double_grid'))
        
        # Create rows for Payee table (Expenses only)
        payee_rows = []
        payee_needs = {}  # Store needed amounts for payment calculations
        for payee in sorted(payee_totals.keys()):  # Sort payees alphabetically
            payee_data = payee_totals[payee]
            
            # Calculate A and B for this payee (Expenses only)
            payee_a = payee_data['M'] / 2 + round(payee_data['A'], 2)
            payee_b = payee_data['M'] / 2 + round(payee_data['B'], 2)
            
            # Calculate needed amounts
            needed_a = split_disposable_a + abs(payee_a)
            needed_b = split_disposable_b + abs(payee_b)
            
            # Store for payment calculations
            payee_needs[payee] = {'A': needed_a, 'B': needed_b}
            
            # Create row dictionary
            payee_row = {
                'Payee': payee,
                'Total': format_value(payee_data['total']),
                'A Expenses': format_value(payee_a),
                'B Expenses': format_value(payee_b),
                'A Needs': format_value(round(needed_a, 2)),
                'B Needs': format_value(round(needed_b, 2))
            }
            payee_rows.append(payee_row)
        
        # Print the Payee table
        print("\nCashflow by Payee (Expenses):")
        print(tabulate(payee_rows, headers='keys', tablefmt='double_grid'))
        
        # Determine payments based on greatest need for each pay period
        print("\nPayment Assignments:")
        for period in ['A', 'B']:
            # Find payee with greatest need (highest positive Needed value)
            needs = [(payee, data[period]) for payee, data in payee_needs.items()]
            needs.sort(key=lambda x: x[1], reverse=True)  # Sort by need descending
            
            if not needs or needs[0][1] <= 0:
                print(f"For pay period {period}, no payee needs additional funds.")
                continue
            
            max_need_payee, max_need = needs[0]
            rounded_max_need = round(max_need,2)
            # Adjust need by the payee's own income
            max_need_income_half = payee_income.get(max_need_payee, 0) / 2
            net_need = rounded_max_need - max_need_income_half
            if net_need <= 0:
                print(f"For pay period {period}, {max_need_payee}'s need of ${rounded_max_need:.2f} is covered by their income of ${max_need_income_half:.2f}.")
                continue
            
            print(f"For pay period {period}, {max_need_payee} needs ${net_need:.2f} after their income of ${max_need_income_half:.2f}.")
            
            # Calculate surplus for other payees: (income / 2) - Needed
            surplus_payees = []
            for payee, need in needs:
                if payee == max_need_payee:
                    continue
                income_half = payee_income.get(payee, 0) / 2
                surplus = income_half - need
                if surplus > 0:
                    surplus_payees.append((payee, surplus))
            
            if not surplus_payees:
                print(f"No payees have surplus to cover {max_need_payee}'s need in pay period {period}.")
                continue
            
            # Distribute the net need among surplus payees
            remaining_need = net_need
            for payee, surplus in sorted(surplus_payees, key=lambda x: x[1], reverse=True):  # Sort by surplus descending
                if remaining_need <= 0.0:
                    break
                # Calculate how much this payee should pay (proportional to their surplus)
                contribution = min(surplus, remaining_need)
                if contribution > 0.0:
                    print(f"  {payee} should pay ${contribution:.2f} to {max_need_payee}.")
                    remaining_need -= round(contribution,2)
            if remaining_need > 0.0:
                print(remaining_need)
                print(f"  Remaining need of ${remaining_need:.2f} for {max_need_payee} could not be covered.")
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
                    added_cashflow = Cashflow(self)
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
    
    def display_expense_plan_menu(self):
        """ Displays the expense plan menu for managing cashflows and people. """
        while True:
            clear_screen()
            print('Edit Expense Plan Menu')
            print("===========================")
            print('(1) Cashflow Management')
            print('(2) People Management')
            print('(3) List cashflows')
            print('(4) Show total of cashflows')
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
                            self.cashflow_management()
                            break 
                case '2':
                    print(self.people)
                    getchit()
                case '3':
                    clear_screen()
                    print('\nAll cashflow:')
                    self.print_cashflow()
                    input("Press any key to continue")
                case '4':
                    clear_screen()
                    self.total_cashflow()
                    input("Press any key to continue")
                case 'q':
                    try:
                        return self
                    except UnboundLocalError:
                        print("Return failed")
                        break
    def accumulate_cashflows(self):
        """ Accumulates cashflows from all people into the expense plan's cashflows list. """
        self.cashflows = []  # Clear existing cashflows
        print(self.people)
        for person in self.people:
            person_dict = person.__dict__
            print(person_dict)
            for cashflow in person_dict['cashflows']:
                self.cashflows.append(cashflow)