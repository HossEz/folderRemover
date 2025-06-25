## Description
This script processes `.zip`, `.rar`, `.7z` files and regular folders by extracting their contents, removing any nested directories, and consolidating all files into a single directory.
The processed files are saved in the `Result` folder.

## Requirements
- Python
- Required Python libraries:
  - colorama
  - py7zr
  - rarfile

## How to Use
1. Place your `.zip`, `.rar`, `.7z` files or folders in the same directory as this script.
2. Run the `run.bat` file.
3. The script will check for the necessary requirements and install them if needed.
4. The script will process the files and save the results in the `Result` folder.
5. The original files and folders will be deleted after processing, and all consolidated files will be placed in the Result folder.

## Uninstall
Uninstalls the required Python libraries.

Made by hosse