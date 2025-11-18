from tools import *
from objects.Engine import Engine
import os


folder_path: str = "saves/"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

def main():
    engine = Engine()
    engine.run()
    
if __name__ == "__main__":
    main()