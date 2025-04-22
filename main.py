import cashflow
import getch
import os
import getfiles
import ast

folder_path = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    print("Welcome to Expense Tracker")
    print("(S)tart Fresh or (L)oad?")
    loaded_file = None
    choice = getch.getch()
    if choice == "s":
        filename = input("Enter a name for the new file: ")
        loaded_cashflow = {"filename": filename, "cashflows":[], "people": []} 
    elif choice == "l":
        files = getfiles.get_file_names("saves/")
        print(files)
        for each in files:
            print(each)
        while True:
            file = input("Enter file name: ")
            if file in files:
                filename = file
                loaded_file = cashflow.load_cashflow(file)
                loaded_cashflow = ast.literal_eval(loaded_file)
                break
            else:
                print(file+" does not exist. Please try again.")
    while True:
        print("Expense Tracker Main Menu")
        print("Current File: "+loaded_cashflow['filename'])
        print("(1) Show Loaded File (Temporary)")
        print("(2) View Statistics")
        print("(3) Edit Cashflow")
        print("(q) Exit")
        choice = getch.getch()
        match(choice):
            case "1":
                try:
                    cashflow.print_cashflow(loaded_cashflow)
                except UnboundLocalError:
                    print("No file loaded.")
                    input()
            case "2":
                pass
            case "3":
                loaded_cashflow = cashflow.cashflowed(filename, loaded_cashflow)
            case "q":
                break
main()