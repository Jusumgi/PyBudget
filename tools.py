import os
import platform

system = platform.system()
def getchit()-> str:
    """
    Allows for character input for faster UI experience, no matter which platform the script is run on.
    """
    if system == "Windows":
        import msvcrt
        byte_input = msvcrt.getch()
        string_input = byte_input.decode('ascii')
        return string_input
    elif system == 'Linux' or system == "Darwin":
        import getch
        return getch.getch()
    else:
        print("Operating System not supported")
def clear_screen():
    """
    Allows for clear screen to occur no matter which platform the script is run on.
    """
    if system == "Windows":
        os.system('cls')
    elif system == "Linux" or system == "Darwin":
        os.system('clear')
    else:
        print("Operating System not supported")

def createFolder(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_file_names(folder_path: str) -> list:
  """
    Returns a list of file names in the specified folder.
    
    Args:
        folder_path: The path to the folder.
    
    Returns:
        A list of strings, where each string is a file name.
  """
  try:
    all_entries = os.listdir(folder_path)
    file_names = [entry.removesuffix(".pkl") for entry in all_entries if os.path.isfile(os.path.join(folder_path, entry))]
    return file_names
  except FileNotFoundError:
    return f"Error: Folder not found at path: {folder_path}"
  except NotADirectoryError:
    return f"Error: Not a directory: {folder_path}"

def initialize_expenseplan_menu():
    from objects.ExpensePlan import ExpensePlan
    import pickle
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