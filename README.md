# FileCollapser

FileCollapser is a Python project that allows you to collapse to quickly remove all files from a folder structure.

## Features

- **Folder Collapsing**: Move all files inside folder / sub-folders into one.
- **Customizable Options**: Choose whether to move, copy, delete directories
- **Context Menu Integration**: embed into File Explorer Context menu

## Installation

To use FileCollapser, follow these steps:

1. Clone the repository: `git clone https://github.com/your-username/FileCollapser.git`
2. Navigate to the project directory: `cd FileCollapser`
3. Compile using command `pyinstaller main.py --onefile --icon=icon.ico --name==CollapseFolder`
4. To install to context menu, Navigate to the project directory: `cd FileCollapser` in administrator
5. Run `CollapseFolder -install`

## Usage

To collapse folders using FileCollapser, run the following command:

```
FolderCollapser /path/to/folder
```

Replace `/path/to/folder` with the path to a folder you want to collapse.

## Arguments

- **-install**: Install the script into the Windows context menu.
- **-move** or **-m**: Move files from the specified directory to its parent directory (default operation).
- **-copy** or **-c**: Copy files from the specified directory to its parent directory.
- **-delete** or **-d**: Delete directories after moving or copying files.
- **-recurse x** or **-r x**: Search subdirectories up to x levels deep and move/copy files.
- **-debug**: Print detailed information about the operations being performed.
- **-help** or **-h**: Display the help message.

