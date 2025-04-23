from colorama import Fore, Style
from tabulate import tabulate

def expenseplan(cashflow):
    # Initialize dictionaries to store totals and track payperiods per flow_type
    totals = {}
    payperiods_by_flow = {'Income': set(), 'Expense': set()}
    payee_totals = {}
    payee_income = {}
    
    # Calculate totals and group payperiods by flow_type
    for each in cashflow['cashflows']:
        flow_type = each['flow_type']
        payperiod = each['payperiod']
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
    people = cashflow.get('people', [])
    split_disposable_a = disposable_a / len(people) if people else disposable_a
    split_disposable_b = disposable_b / len(people) if people else disposable_b
    
    # Add formatted A and B values to rows
    income_row['A'] = format_value(half_income)
    income_row['B'] = format_value(half_income)
    expense_row['A'] = format_value(expense_a)
    expense_row['B'] = format_value(expense_b)
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
        payee_a = payee_data['M'] / 2 + payee_data['A']
        payee_b = payee_data['M'] / 2 + payee_data['B']
        
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
                remaining_need -= contribution
        if remaining_need > 0.0:
            print(f"  Remaining need of ${remaining_need:.2f} for {max_need_payee} could not be covered.")