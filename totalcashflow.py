from colorama import Fore, Style
from tabulate import tabulate

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
    
    # Calculate Disposable income (Income - Expense)
    disposable = totals.get('Income', 0) + totals.get('Expense', 0)
    
    # Format totals with color based on value
    for key in totals:
        if totals[key] < 0:
            totals[key] = Fore.RED + '$' + str(totals[key]) + Style.RESET_ALL
        else:
            totals[key] = Fore.GREEN + '$' + str(totals[key]) + Style.RESET_ALL
    
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