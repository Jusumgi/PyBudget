from tools import *
from objects.ExpensePlan import ExpensePlan
import os
import pickle

folder_path: str = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    loaded_expense_plan = initialize_expenseplan_menu()
    while True:
        clear_screen()
        print("Expense Tracker Main Menu")
        print("===========================")
        print("Current File: "+loaded_expense_plan.filename)
        print("(1) View Expense Plan")
        print("(2) View Statistics")
        print("(3) Edit Expense Plan")
        print("(4) Save Expense Plan")
        print("(5) Load Expense Plan")
        print("(q) Exit")
        choice = getchit()
        match(choice):
            case "1":
                loaded_expense_plan.print_expenseplan()
                getchit()
            case "2":
                loaded_expense_plan.total_cashflow()
                getchit()
            case "3":
                loaded_expense_plan: ExpensePlan = loaded_expense_plan.display_expense_plan_menu()
            case "4":
                expenseplan_filename = input("Enter save name: ")
                loaded_expense_plan.filename = expenseplan_filename
                with open("saves/"+expenseplan_filename+".pkl", "wb") as file:
                    pickle.dump(loaded_expense_plan, file)
            case "5":
                print(get_file_names("saves/"))
                expenseplan_filename = input("Enter file name: ")
                try:
                    with open("saves/"+expenseplan_filename+".pkl", "rb") as file:
                        loaded_expense_plan = pickle.load(file)
                except FileNotFoundError:
                    loaded_expense_plan = 5
                if loaded_expense_plan == 5:
                    print("File not found.")
                    input('Press any key to continue')
                else:
                    loaded_expense_plan: ExpensePlan = loaded_expense_plan
                    clear_screen()
                    print("Loaded Expense Plan:")
                    loaded_expense_plan.print_cashflow()
                    input('Press any key to continue')
            case "q":
                break

if __name__ == "__main__":
    main()