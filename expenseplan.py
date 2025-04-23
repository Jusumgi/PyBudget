from colorama import Fore, Style
from tabulate import tabulate

def expenseplan(cashflow):
    # Initialize dictionaries to store totals and track payperiods per flow_type
    totals = {}
    payperiods_by_flow = {'Income': set(), 'Expense': set()}
    
    # Calculate totals and group payperiods by flow_type
    for each in cashflow['cashflows']:
        flow_type = each['flow_type']
        payperiod = each['payperiod']
        amount = each['amount']
        people = cashflow['people']
        payee = each['payee']
        totals[flow_type] = totals.get(flow_type, 0) + amount
        totals[payperiod] = totals.get(payperiod, 0) + amount
        totals[payee] = totals.get(payee, 0) + amount
        payperiods_by_flow[flow_type].add(payperiod)

    income = round(totals.get('Income', 0),2)
    half_income = round(totals.get('I', 0),2) /2
    expense = round(totals.get('Expense', 0),2)
    monthly = round(totals.get('M', 0), 2)
    a_expense = round(totals.get('A', 0),2)
    b_expense = round(totals.get('B', 0),2)
    # Calculate Disposable income (Income - Expense)
    disposable = round(income + expense,2)
    # Helper function to format values with color
    def format_value(value):
        return (
            Fore.RED + '$' + str(value) + Style.RESET_ALL if value < 0
            else Fore.GREEN + '$' + str(value) + Style.RESET_ALL
        )
    
    # Create separate dictionaries for Income, Expense, and Disposable rows
    income_row = {'Type': 'Income', 'Total': format_value(income)}
    expense_row = {'Type': 'Expense', 'Total': format_value(expense)}
    disposable_row = {'Type': 'Disposable', 'Total': format_value(disposable)}
    each_row = {'Type': 'Disp. Split'}
    
    # Expense: Split payperiod M evenly between A and B, add direct A and B expenses
    expense_a = monthly / 2 + a_expense
    expense_b = monthly / 2 + b_expense
    
    # Disposable: Difference between Income and Expense for A and B
    disposable_a = round(half_income + expense_a,2)  # Expense is negative, so add to subtract
    disposable_b = round(half_income + expense_b,2)
    split_disposable_a = disposable_a / len(people)
    split_disposable_b = disposable_b / len(people)
    
    # Add formatted A and B values to rows
    income_row['A'] = format_value(half_income)
    income_row['B'] = format_value(half_income)
    expense_row['A'] = format_value(expense_a)
    expense_row['B'] = format_value(expense_b)
    disposable_row['A'] = format_value(disposable_a)
    disposable_row['B'] = format_value(disposable_b)
    each_row['A'] = format_value(round(split_disposable_a,2))
    each_row['B'] = format_value(round(split_disposable_b, 2))
    
    # Collect rows for tabulate
    rows = [income_row, expense_row, disposable_row, each_row]
    
    # Print the table using tabulate
    if rows:
        print(tabulate(rows, headers='keys', tablefmt='double_grid'))
    else:
        print("No data to display.")