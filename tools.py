import os
import platform
import webbrowser
import json

system = platform.system()
def getchit():
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

def open_pdf(file_path):
    if os.path.exists(file_path):
        webbrowser.open_new(file_path)
        print(f"Opened PDF: {file_path}")
    else:
        print(f"Error: PDF file not found at {file_path}")

def saveFile(data, filename):
    # If the folder isn't created yet, then create it.
    folder_path = "save/"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def loadFile(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return None
def createFolder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_file_names(folder_path):
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