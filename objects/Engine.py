from tools import *
from objects.ExpensePlan import ExpensePlan 
from objects.Person import Person

class Engine:
    """
    The main engine that runs the budgeting application.
    It manages people and their associated expense plans.
    """
    def __init__(self):
        self.people = []
        self.expense_plans = [] # may be used later
        self.current_expense_plan = None
        self.active_person = None

    def run(self):
        self.current_expense_plan = self.initialize_expenseplan_menu()
        while True:
            clear_screen()
            print("Expense Tracker Main Menu")
            print("===========================")
            print("Current File: "+self.current_expense_plan.filename)
            print("Active Person: "+ (self.active_person if self.active_person else "None"))
            print("(1) Manage People")
            print("(2) Manage your Cashflows")
            print("(3) Manage Expense Plan")
            print("(4) View Total Cashflow of Expense Plan")
            print("(5) View Expense Plan")
            print("(6) Save Expense Plan(deprecated)")
            print("(7) Load Expense Plan(deprecated)")
            print("(q) Exit")
            choice = getchit()
            match(choice):
                case "1":
                    self.people_management(self.people)
                    pickle_save(self.people, "saves/people.pkl")
                case "2":
                    if self.active_person is None:
                        print("No active person selected. Please set an active person first.")
                        input("Press any key to continue.")
                    else:
                        for person in self.people:
                            each = person.__dict__
                            if each['name'] == self.active_person:
                                person.cashflow_management()
                case "3":
                    self.current_expense_plan: ExpensePlan = self.current_expense_plan.display_expense_plan_menu()
                case "4":
                    self.current_expense_plan.total_cashflow()
                    getchit()
                case "5":
                    self.current_expense_plan.print_expenseplan()
                    getchit()
                case "6":
                    expenseplan_filename = input("Enter save name: ")
                    self.current_expense_plan.filename = expenseplan_filename
                    pickle_save(self.current_expense_plan, "saves/"+expenseplan_filename+".pkl")
                case "7":
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
        """ Initializes the expense plan by either creating a new one or loading an existing one. """
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
                        loaded_expense_plan = pickle_load("saves/"+file+".pkl")
                        return loaded_expense_plan
                    else:
                        print(file+" does not exist. Please try again.")
            else:
                print("Invalid input")

    def add_people(self):
        """ Adds a person to the expense plan by name. """
        while True:
            person_add: str = input("Enter a name to be added: ")
            if person_add:
                self.people.append(Person(person_add))
                break
            else:
                print("Cannot enter a blank name.")

    def remove_people(self):
        """ Removes a person from program by name. """
        name = input('Enter the name of cashflow to be removed: ')
        found = False
        for index, item in enumerate(self.people):
            each = item.__dict__ # Convert each Person object to dict
            if each['name'] == name:
                found = True
                print(each)
                print("Are you sure you want to remove? (y)es or (n)o")
                while True:
                    confirmation = getchit()
                    if confirmation == 'y':
                        self.people.pop(index)
                        print('Person removed')
                        input("Press any key to continue")
                        break
                    elif confirmation == 'n' :
                        print('Person not removed.')
                        input("Press any key to continue")
                        break
                    else:
                        print("Please press y or n")
                break        
        if not found:
            print(f"Person with name '{name}' not found.")
            input("Press any key to continue")

    def people_management(self, people: list):
        """ Manages adding and removing people from the expense plan. """
        while True:
            clear_screen()
            print("Current People")
            for each in people:
                each = each.__dict__
                print(each['name'])
            print(f"(1) Set Active Person : {self.active_person if self.active_person else 'None'}")
            print("(2) Add/Remove Person")
            print("(b) Back to Main Menu")
            choice = getchit()
            match(choice):
                case "1":
                    name = input("Enter the name of the person to set as active: ")
                    for person in self.people:
                        each = person.__dict__
                        if each['name'] == name:
                            self.active_person = name
                            print(f"Active person set to {name}.")
                            input("Press any key to continue.")
                            break
                    else:
                        print(f"Person with name '{name}' not found.")
                        input("Press any key to continue.")
                case "2":
                    self.add_remove_person()
                case "b":
                    break
    def add_remove_person(self):
        """ Manages adding and removing people from the expense plan. """
        while True:
            clear_screen()
            print("Current People")
            for each in self.people:
                each = each.__dict__
                print(each['name'])
            print("(a)dd or (r)emove people?")
            print("Press b to go back")
            peepmgmt = getchit()
            match(peepmgmt):
                case 'a':
                    self.add_people()  
                case 'r':
                    if len(self.people) == 0:
                        print("No people to remove.")
                        input("Press any key to continue.")
                    else:
                        self.remove_people()
                case 'b':
                    break