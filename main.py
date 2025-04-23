from cashflowtools import *
from totalcashflow import total_cashflow
from getfiles import get_file_names
from cashflowmgmt import load_cashflow, print_cashflow
from cashflow import cashflow
from expenseplan import expenseplan
import os
import ast

folder_path = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    clear_screen()
    print("Welcome to Expense Tracker")
    print("(S)tart Fresh or (L)oad?")
    loaded_file = None
    choice = getchit()
    if choice == "s":
        filename = input("Enter a name for the new file: ")
        loaded_cashflow = {"filename": filename, "cashflows":[], "people": []} 
    elif choice == "l":
        files = get_file_names("saves/")
        print(files)
        for each in files:
            print(each)
        while True:
            file = input("Enter file name: ")
            if file in files:
                filename = file
                loaded_file = load_cashflow(file)
                loaded_cashflow = ast.literal_eval(loaded_file)
                break
            else:
                print(file+" does not exist. Please try again.")
    while True:
        clear_screen()
        print("Expense Tracker Main Menu")
        print("===========================")
        print("Current File: "+loaded_cashflow['filename'])
        print("(1) View Expense Plan")
        print("(2) View Statistics")
        print("(3) Edit Cashflow")
        print("(q) Exit")
        choice = getchit()
        match(choice):
            case "1":
                try:
                    clear_screen()
                    expenseplan(loaded_cashflow)
                    getchit()
                except UnboundLocalError:
                    print("No cashflow loaded.")
                    getchit()
            case "2":
                try:
                    clear_screen()
                    total_cashflow(loaded_cashflow)
                    getchit()
                except KeyError:
                    print("No cashflow loaded.")
                    getchit()
            case "3":
                loaded_cashflow = cashflow(filename, loaded_cashflow)
            case "q":
                break
main()