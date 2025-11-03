from totalcashflow import total_cashflow
from cashflowmgmt import *
from tools import clear_screen, get_file_names
import ast

def add_people(cashflow):
    while True:
        person_add = input("Enter a name to be added: ")
        if person_add:
            cashflow['people'].append(person_add)
            break
        else:
            print("Cannot enter a blank name.")

def remove_people(cashflow):
    person_remove = input("Enter a name to be removed: ")
    try:
        index = cashflow['people'].index(person_remove)
        cashflow['people'].pop(index)
    except ValueError:
        print("Name not found")

def people_management(cashflow):
    while True:
        clear_screen()
        print("Current People")
        for each in cashflow['people']:
            print(each)
        print("(a)dd or (r)emove people?")
        print("Press b to go back")
        peepmgmt = getchit()
        match(peepmgmt):
            case 'a':
                add_people(cashflow)  
            case 'r':
                if len(cashflow['people']) == 0:
                    print("No people added")
                    input("Press any key to continue.")
                else:
                    remove_people(cashflow)
            case 'b':
                break


def cashflow_menu(filename, loaded_cashflow):
    cashflow = {"filename": filename, "cashflows":loaded_cashflow['cashflows'], "people": loaded_cashflow['people']}
    try:
        with open("saves/people.txt") as file:
                people = ast.literal_eval(file.read())
                print(people)
    except FileNotFoundError:
        pass
    while True:
        clear_screen()
        print('Edit Cashflow Menu')
        print("===========================")
        print('(1) Cashflow Management')
        print('(2) People Management')
        print('(3) List cashflow')
        print('(4) Show total cashflow')
        print('(5) Save Cashflow')
        print('(6) Load Cashflow | Current File: '+cashflow['filename'])
        print('(q) Exit')
        print('--------------------------------')
        print('Select an option')
        choice = getchit()

        match(choice):
            case '1':
                while True:
                    if not cashflow['people']:
                        print("Please add people first.")
                        getchit()
                        break
                    else:
                        cashflow_management(cashflow)
                        break 
            case '2':
                people_management(cashflow)
            case '3':
                clear_screen()
                print('\nAll cashflow:')
                print_cashflow(cashflow)
                input("Press any key to continue")
            case '4':
                clear_screen()
                # print('\nTotal cashflow: ', total_cashflow(cashflow))
                total_cashflow(cashflow)
                input("Press any key to continue")
            case '5':
                save_cashflow(cashflow)
            case '6':
                clear_screen()
                print(get_file_names("saves/"))
                cashflow_filename = input("Enter file name: ")
                loaded_file = load_cashflow(cashflow_filename)
                if loaded_file == 5:
                    clear_screen()
                    print("File was not found.")
                    input('Press any key to continue')
                else:
                    cashflow = ast.literal_eval(loaded_file)
                    clear_screen()
                    print_cashflow(cashflow)
                    input('Press any key to continue')
            case 'q':
                try:
                    return cashflow
                except UnboundLocalError:
                    print("Return failed")
                    break
