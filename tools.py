import os
import platform
import pickle

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

def pickle_save(obj, filepath: str):
    """ Saves an object to a file using pickle serialization. """
    with open(filepath, "wb") as file:
        pickle.dump(obj, file)
def pickle_load(filepath: str):
    """ Loads an object from a file using pickle serialization. """
    try:
        with open(filepath, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at path: {filepath}")
        return None
    
def currency_symbol_selection():
    """ Prompts user to select a currency symbol. """
    symbols = {
        '1': '$',  # US Dollar
        '2': '€',  # Euro
        '3': '£',  # British Pound
        '4': '¥',  # Japanese Yen
        '5': '₹',  # Indian Rupee
        '6': '₽'   # Russian Ruble
    }
    print("Select a currency symbol:")
    for key, symbol in symbols.items():
        print(f"({key}) {symbol}")
    
    while True:
        choice = getchit()
        if choice in symbols:
            return symbols[choice]
        else:
            print("Invalid choice. Please select a valid option.")

def prompt_save(obj, filepath: str, description: str = "current data") -> bool:
    """
    Prompts user to save an object before continuing.
    
    Args:
        obj: The object to save.
        filepath: The file path where the object will be saved.
        description: A description of what is being saved (default: "current data").
    
    Returns:
        True if saved, False if user chose not to save.
    """
    while True:
        print(f"Save {description}? (y)es or (n)o")
        choice = getchit().lower()
        if choice == 'y':
            pickle_save(obj, filepath)
            print(f"{description} saved successfully.")
            input("Press any key to continue.")
            return True
        elif choice == 'n':
            print(f"{description} not saved.")
            input("Press any key to continue.")
            return False
        else:
            print("Please press (y) for yes or (n) for no.")