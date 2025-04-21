import os

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
    file_names = [entry.removesuffix(".txt") for entry in all_entries if os.path.isfile(os.path.join(folder_path, entry))]
    return file_names
  except FileNotFoundError:
    return f"Error: Folder not found at path: {folder_path}"
  except NotADirectoryError:
    return f"Error: Not a directory: {folder_path}"

# # Example usage
# folder_path = "/saves/"  # Replace with the actual path to your folder
# files = get_file_names(folder_path)

# if isinstance(files, list):
#     print("Files in folder:")
#     for file_name in files:
#         print(file_name)
# else:
#     print(files)