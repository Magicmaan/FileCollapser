import os
import sys
import glob
import shutil


folderpath = "E:\\theob\\Documents\\Python Projects\\FileCollapser\\testpath\\buh"

def help():
    print("Usage: main.py path/to/folder")
    print("-install: Install into context menu")
    print("-move: Moves files to parent directory")
    print("-copy: Copies files to parent directory")
    print("-delete: delete folder paths")
    print("-recurse x: search subdirectories x levels deep and move/copy files")
    sys.exit(1)

def install():
    #TODO: Implement install function
    #Add registry key to context menu
    #set default args to -move -recurse *
    pass

def main() -> None:
    operation = "move"
    recursion_depth = 0
    delete_directories = True
    debug = True

    args = sys.argv[1:]
    if len(args) < 1:
        help()
    if ("-help" or "-h") in args:
        help()

    if ("-install") in args:
        install()


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
    if not os.path.exists(folderpath):
        print(f"Error: Folder {folderpath} does not exist.")
        help()
        sys.exit(1)

    folderpath += "\\*"
    destination = folderpath + "\\.."

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


def getFiles(directory: str,depth=1) -> tuple[list[str], list[str]]:
    files:list[str] = []
    directories:list[str] = []

    for file in glob.glob(directory):
        if os.path.isfile(file):
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
        shutil.move(current_path,destination_path)    
    except Exception as e:
        print(f"Error: {e}")

def copyFile(current_path: str,destination_path:str) -> None:
    try:
        shutil.copy(current_path,destination_path)    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
