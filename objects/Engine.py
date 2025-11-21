from tools import *
from objects.ExpensePlan import ExpensePlan 
from objects.Person import Person

class Engine:
    """
    The main engine that runs the budgeting application.
    It manages people and their associated expense plans.
    """
    def __init__(self, filename):
        self.filename = filename
        self.people = []
        self.expense_plans = [] # may be used later
        self.current_expense_plan = None
        self.active_person = None

    def run(self):
        while True:
            clear_screen()
            print("Expense Tracker Main Menu")
            print("===========================")
            print("Current File: "+self.filename)
            print("Active Person: "+ (self.active_person if self.active_person else "None"))
            print("Current Expense Plan: "+ (self.current_expense_plan.plan_name if self.current_expense_plan else "None"))
            print("===========================")
            print("(1) Manage People")
            print("(2) Manage your Cashflows")
            print("(3) Manage Expense Plan")
            print(f"(4) View Total Cashflow of {self.active_person if self.active_person else 'No Active Person'}")
            print("(5) View Expense Plan")
            print("(6) Save File")
            print("(7) Load File")
            print("(q) Exit")
            choice = getchit()
            match(choice):
                case "1":
                    self.people_management(self.people)
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
                    if self.current_expense_plan is None:
                        print("No expense plan loaded.")
                        self.current_expense_plan = self.create_expense_plan()
                    else:
                        self.current_expense_plan = self.expense_plan_management()
                case "4":
                    if self.active_person is None:
                        print("No active person selected. Please set an active person first.")
                        input("Press any key to continue.")
                    else:
                        for person in self.people:
                            each = person.__dict__
                            if each['name'] == self.active_person:
                                person.total_cashflow()
                    getchit()
                case "5":
                    if self.current_expense_plan is None:
                        print("No expense plan loaded.")
                        self.current_expense_plan = self.create_expense_plan()
                    else:
                        self.current_expense_plan.print_expenseplan()
                        getchit()
                case "6":
                    save_file = input("Enter save name: ")
                    pickle_save(self, "saves/"+save_file+".pkl")
                case "7":
                    prompt_save(self, self.filename, "current session")
                    print(get_file_names("saves/"))
                    save_file = input("Enter file name: ")
                    self = pickle_load("saves/"+save_file+".pkl")
                    self: Engine = self
                case "q":
                    prompt_save(self, self.filename, "current session")
                    break

    def add_people(self):
        """ Adds a person to the program by name. """
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
            print("(2) Set Currency Symbol for Active Person")
            print("(3) Add/Remove Person")
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
                    if self.active_person is None:
                        print("No active person selected. Please set an active person first.")
                        input("Press any key to continue.")
                    else:
                        for person in self.people:
                            each = person.__dict__
                            if each['name'] == self.active_person:
                                print(f"Current currency symbol for {self.active_person}: {each['currency_symbol']}")
                                person.change_currency_symbol()
                case "3":
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
    def select_people(self):
        """ Selects people to be included in the expense plan. """
        selection = input("Add all people to expense plan? (y)es or (n)o:")
        if selection.lower() == 'y':
            return self.people
        selected_people = []
        for each in self.people:
            each = each.__dict__
            print(each['name'])
        print("Select people to include in the expense plan:")
        while True:
            name = input("Enter person's name or 'done' when finished: ")
            for index, item in enumerate(self.people):
                each = item.__dict__ # Convert each Person object to dict
                if each['name'] == name:
                    selected_people.append(self.people[index])
                    print(f'{each['name']} added')
                    break   
            if name.lower() == 'done':
                break
        return selected_people
    
    def create_expense_plan(self, current_expense_plan=None):
        print("Would you like to create one now? (y)es or (n)o")
        while True:
            confirmation = getchit()
            if confirmation == 'y':
                plan_name = input("Enter a name for the new expense plan: ")
                self.current_expense_plan = ExpensePlan(plan_name, self.select_people())
                self.current_expense_plan.accumulate_cashflows()
                self.expense_plans.append(self.current_expense_plan)
                print(f"Expense Plan '{plan_name}' created and loaded.")
                input("Press any key to continue.")
                return self.current_expense_plan
            elif confirmation == 'n':
                print("Returning to main menu.")
                input("Press any key to continue.")
                return current_expense_plan
            else:
                print("Please press y or n")
    def select_expense_plan(self):
        """ Selects an existing expense plan to be the current one. """
        if len(self.expense_plans) == 0:
            print("No expense plans available. Please create one first.")
            input("Press any key to continue.")
            return None
        print("Available Expense Plans:")
        for index, plan in enumerate(self.expense_plans):
            print(f"({index + 1}) {plan.plan_name}")
        while True:
            try:
                selection = int(input("Enter the number of the expense plan to load: "))
                if 1 <= selection <= len(self.expense_plans):
                    self.current_expense_plan = self.expense_plans[selection - 1]
                    print(f"Expense Plan '{self.current_expense_plan.plan_name}' loaded.")
                    input("Press any key to continue.")
                    return self.current_expense_plan
                else:
                    print(f"Please enter a number between 1 and {len(self.expense_plans)}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def delete_expense_plan(self):
        """ Deletes the current expense plan. """
        if self.current_expense_plan is None:
            print("No expense plan loaded. Cannot delete.")
            input("Press any key to continue.")
            return
        print("Are you sure you want to delete the current expense plan? (y)es or (n)o")
        while True:
            confirmation = getchit()
            if confirmation == 'y':
                print(f"Expense Plan '{self.current_expense_plan.plan_name}' deleted.")
                self.current_expense_plan = None
                input("Press any key to continue.")
                return
            elif confirmation == 'n' :
                print('Expense Plan not deleted.')
                input("Press any key to continue.")
                return
            else:
                print("Please press y or n")

    def expense_plan_management(self):
        """ Manages the current expense plan. """
        if self.current_expense_plan is None:
            print("No expense plan loaded. Please create or load an expense plan first.")
            input("Press any key to continue.")
            return
        while True:
            clear_screen()
            print(f"Expense Plan: {self.current_expense_plan.plan_name if self.current_expense_plan else 'None'}")
            print(f"(1) View Expense Plan")
            print(f"(2) Set Currency Symbol: {self.current_expense_plan.currency_symbol}")
            print(f"(3) Set Pay Period: {self.current_expense_plan.payperiod_selector}")
            print("==========================")
            print(f"(4) Create New Expense Plan")
            print(f"(5) Change Expense Plan")
            print(f"(6) Delete Expense Plan")
            print("(b) Back to Main Menu")
            choice = getchit()
            match(choice):
                case "1":
                    self.current_expense_plan.print_expenseplan()
                    getchit()
                case "2":
                    self.current_expense_plan.change_currency_symbol()
                case "3":
                    self.current_expense_plan.set_pay_period()
                case "4":
                    self.current_expense_plan = self.create_expense_plan(self.current_expense_plan)
                case "5":
                    self.select_expense_plan()
                case "6":
                    print("Are you sure you want to delete the current expense plan? (y)es or (n)o")
                    while True:
                        confirmation = getchit()
                        if confirmation == 'y':
                            print(f"Expense Plan '{self.current_expense_plan.plan_name}' deleted.")
                            self.current_expense_plan = None
                            input("Press any key to continue.")
                            return None
                        elif confirmation == 'n' :
                            print('Expense Plan not deleted.')
                            input("Press any key to continue.")
                            break
                        else:
                            print("Please press y or n")
                case "b":
                    return self.current_expense_plan