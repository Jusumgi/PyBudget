from tools import *
from ExpensePlan import ExpensePlan
import os
import pickle

folder_path: str = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    clear_screen()
    print("Welcome to Expense Tracker")
    print("(S)tart Fresh or (L)oad?")
    loaded_file = None
    while True:
        choice = getchit()
        if choice == "s":
            filename = input("Enter a name for the new file: ")
            loaded_cashflow: ExpensePlan = ExpensePlan(filename)
            break
        elif choice == "l":
            files = get_file_names("saves/")
            print(files)
            for each in files:
                print(each)
            while True:
                file = input("Enter file name: ")
                if file in files:
                    with open("saves/"+file+".pkl", "rb") as f:
                        loaded_cashflow = pickle.load(f)
                    print(loaded_cashflow)
                    break
                else:
                    print(file+" does not exist. Please try again.")
            break
        else:
            print("Invalid input")
    while True:
        clear_screen()
        print("Expense Tracker Main Menu")
        print("===========================")
        print("Current File: "+loaded_cashflow.filename)
        print("(1) View Expense Plan")
        print("(2) View Statistics")
        print("(3) Edit Expense Plan")
        print("(4) Save Expense Plan")
        print("(5) Load Expense Plan")
        print("(q) Exit")
        choice = getchit()
        match(choice):
            case "1":
                try:
                    clear_screen()
                    loaded_cashflow.print_expenseplan()
                    getchit()
                except UnboundLocalError:
                    print("No cashflow loaded.")
                    getchit()
            case "2":
                try:
                    clear_screen()
                    loaded_cashflow.total_cashflow()
                    getchit()
                except KeyError:
                    print("No cashflow loaded.")
                    getchit()
            case "3":
                loaded_cashflow: ExpensePlan = loaded_cashflow.display_expense_plan_menu()
            case "4":
                expenseplan_filename = input("Enter save name: ")
                loaded_cashflow.filename = expenseplan_filename
                with open("saves/"+expenseplan_filename+".pkl", "wb") as file:
                    pickle.dump(loaded_cashflow, file)
            case "5":
                print(get_file_names("saves/"))
                expenseplan_filename = input("Enter file name: ")
                try:
                    with open("saves/"+expenseplan_filename+".pkl", "rb") as file:
                        loaded_file = pickle.load(file)
                except FileNotFoundError:
                    loaded_file = 5
                if loaded_file == 5:
                    print("File not found.")
                    input('Press any key to continue')
                else:
                    loaded_cashflow: ExpensePlan = loaded_file
                    clear_screen()
                    print("Loaded Expense Plan:")
                    loaded_cashflow.print_cashflow()
                    input('Press any key to continue')
            case "q":
                break

if __name__ == "__main__":
    main()