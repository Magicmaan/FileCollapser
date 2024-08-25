import sys
import winreg
from os import path
from glob import glob
from shutil import move, copy


def help():
    print("Usage: main path/to/folder")
    print("-install: Install into context menu")
    print("-move: Moves files to parent directory")
    print("-copy: Copies files to parent directory")
    print("-delete: delete folder paths")
    print("-recurse x: search subdirectories x levels deep and move/copy files")
    sys.exit(1)

def get_executable_path():
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # sets the sys.frozen attribute and stores the path to the bundle
        # directory in sys._MEIPASS.
        return sys.executable
    else:
        # If the application is run as a script, use the script directory.
        return path.abspath(__file__)

def install() -> bool:
    #TODO: Implement install function
    #Add registry key to context menu
    #set default args to -move -recurse *

    # Define the registry key paths

    print(f"Executable path: {get_executable_path()}")
    #Computer\HKEY_CLASSES_ROOT\Directory\Background\shell
    app_name = "Collapse Folder"
    app_path = get_executable_path()
    icon_path = app_path

    key_path = r"Directory\shell\CollapseFolder"
    command_key_path = key_path + r"\command"

    try:
        # Create a new key for the application
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)

        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValue(registry_key, '', winreg.REG_SZ, app_name)
        

        winreg.SetValueEx(registry_key, 'Icon', 0, winreg.REG_SZ, icon_path)
        winreg.CloseKey(registry_key)

        # Create a new command key for the application
        winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_key_path)
        registry_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, command_key_path, 0, winreg.KEY_WRITE)
        winreg.SetValue(registry_key, '', winreg.REG_SZ, f'"{app_path}" "%1" "-m"')
        winreg.CloseKey(registry_key)

        print(f'Successfully added {app_name} to the context menu.')

    except Exception as e:
        print(f'Failed to add to context menu: {e}')
    pass

def main() -> None:
    operation = "move"
    recursion_depth = 0
    delete_directories = True
    debug = False

    args = sys.argv[1:]
    if len(args) < 1:
        help()
        return
    if ("-help" or "-h") in args:
        help()
        return

    if ("-install") in args:
        install()
        return

    #set operation type
    if ("-move" or "-m") in args:
        operation = "move"
    elif ("-copy" or "-c") in args:
        operation = "copy"
    
    #set debug mode
    if ("-debug") in args:
        debug = True
    
    #recursion depth
    if ("-recurse" or "-r") in args:
        recursion_depth = args[args.index("-recurse")+1]
    
    if ("-delete" or "-d") in args:
        delete_directories = True

    folderpath = sys.argv[1].lower()
    if not path.exists(folderpath):
        print(f"Error: Folder {folderpath} does not exist.")
        help()
        sys.exit(1)

    destination = folderpath + "\\.." #parent directory
    folderpath += "\\*"
    

    if debug:
        print(f"Folderpath: {folderpath}")
        print(f"Destination: {destination} \n")

        print(f"Operation: {operation}")
        print(f"Recursion Depth: {recursion_depth}")
        print(f"Delete Directories: {delete_directories} \n")

    file_list, directory_list = getFiles(folderpath)

    if operation == "move":
        for file in file_list:
            moveFile(file,destination)
    elif operation == "copy":
        for file in file_list:
            copyFile(file,destination)
    
    if debug:
        print(f"Files: {file_list}")
        print(f"Directories: {directory_list}")
        input("Press Enter to continue...")


def getFiles(directory: str,depth=1) -> tuple[list[str], list[str]]:
    files:list[str] = []
    directories:list[str] = []

    for file in glob(directory):
        if path.isfile(file):
            files.append(file)
        else:
            directories.append(file)
    
    if not files:
        #recursive call to get files from subdirectories, if no files exist in current directory
        for directory in directories:
            f,d = getFiles(directory + "\\*",depth+1)
            files.extend(f)
            directories.extend(d)
    return files, directories
    
def moveFile(current_path: str,destination_path:str) -> None:
    try:
        move(current_path,destination_path)    
    except Exception as e:
        print(f"Error: {e}")


def copyFile(current_path: str,destination_path:str) -> None:
    try:
        copy(current_path,destination_path)    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
