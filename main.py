import cashflow
import getch
import os
import getfiles
import copy

folder_path = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    print("Welcome to Expense Tracker")
    print("(S)tart Fresh or (L)oad?")
    choice = getch.getch()
    if choice == "s":
        pass
    elif choice == "l":
        files = getfiles.get_file_names("saves/")
        for each in files:
            print(each)
        file = input("Enter file name: ")
        loaded_file = cashflow.load_cashflow(file)
    while True:
        print("Expense Tracker Main Menu")
        print("(1) Show Loaded File (Temporary)")
        print("(2) View Statistics")
        print("(3) Edit Cashflow")
        print("(q) Exit")
        choice = getch.getch()
        match(choice):
            case "1":
                print(loaded_file)
            case "2":
                pass
            case "3":
                loaded_file = cashflow.cashflowed()
            case "q":
                break
main()