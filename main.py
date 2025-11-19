from tools import *
from objects.Engine import Engine
import os


folder_path: str = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    engine = initialize_engine_menu()
    engine.run()

def initialize_engine_menu():
    """ Initializes the program engine by either creating a new one or loading an existing one. """
    clear_screen()
    print("Welcome to Expense Tracker")
    print("(S)tart Fresh or (L)oad?")
    loaded_file = None
    while True:
        choice = getchit()
        if choice == "s":
            filename = input("Enter a name for the new file: ")
            loaded_file: Engine = Engine(filename)
            return loaded_file
        elif choice == "l":
            files = get_file_names("saves/")
            print(files)
            for each in files:
                print(each)
            while True:
                file = input("Enter file name: ")
                if file in files:
                    loaded_file: Engine = pickle_load("saves/"+file+".pkl")
                    return loaded_file
                else:
                    print(file+" does not exist. Please try again.")
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()