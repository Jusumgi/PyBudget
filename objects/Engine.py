from tools import *
import pickle
from objects.ExpensePlan import ExpensePlan 

class Engine:
    """
    The main engine that runs the budgeting application.
    It manages people and their associated expense plans.
    """
    def __init__(self):
        self.people = []
        self.expense_plans = [] # may be used later
        self.current_expense_plan = None

    def run(self):
        self.current_expense_plan = self.initialize_expenseplan_menu()
        while True:
            clear_screen()
            print("Expense Tracker Main Menu")
            print("===========================")
            print("Current File: "+self.current_expense_plan.filename)
            print("(1) View Expense Plan")
            print("(2) View Statistics")
            print("(3) Edit Expense Plan")
            print("(4) Save Expense Plan")
            print("(5) Load Expense Plan")
            print("(q) Exit")
            choice = getchit()
            match(choice):
                case "1":
                    self.current_expense_plan.print_expenseplan()
                    getchit()
                case "2":
                    self.current_expense_plan.total_cashflow()
                    getchit()
                case "3":
                    self.current_expense_plan: ExpensePlan = self.current_expense_plan.display_expense_plan_menu()
                case "4":
                    expenseplan_filename = input("Enter save name: ")
                    self.current_expense_plan.filename = expenseplan_filename
                    pickle_save(self.current_expense_plan, "saves/"+expenseplan_filename+".pkl")
                case "5":
                    print(get_file_names("saves/"))
                    expenseplan_filename = input("Enter file name: ")
                    self.current_expense_plan = pickle_load("saves/"+expenseplan_filename+".pkl")
                    if self.current_expense_plan == None:
                        input('Press any key to continue')
                    else:
                        self.current_expense_plan: ExpensePlan = self.current_expense_plan
                        clear_screen()
                        print("Loaded Expense Plan:")
                        self.current_expense_plan.print_cashflow()
                        input('Press any key to continue')
                case "q":
                    break
    
    def initialize_expenseplan_menu(self):
        clear_screen()
        print("Welcome to Expense Tracker")
        print("(S)tart Fresh or (L)oad?")
        loaded_expense_plan = None
        while True:
            choice = getchit()
            if choice == "s":
                filename = input("Enter a name for the new file: ")
                loaded_expense_plan: ExpensePlan = ExpensePlan(filename)
                return loaded_expense_plan
            elif choice == "l":
                files = get_file_names("saves/")
                print(files)
                for each in files:
                    print(each)
                while True:
                    file = input("Enter file name: ")
                    if file in files:
                        with open("saves/"+file+".pkl", "rb") as f:
                            loaded_expense_plan = pickle.load(f)
                        print(loaded_expense_plan)
                        return loaded_expense_plan
                    else:
                        print(file+" does not exist. Please try again.")
            else:
                print("Invalid input")