import cashflow
import getch
import os

folder_path = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    while True:
        print("Expense Tracker Main Menu")
        print("(1) View Plan")
        print("(2) View Statistics")
        print("(3) Edit Cashflow")
        print("(q) Exit")
        choice = getch.getch()
        match(choice):
            case "1":
                pass
            case "2":
                pass
            case "3":
                cashflow.cashflowed()
            case "q":
                break
main()