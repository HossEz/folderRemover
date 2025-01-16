import zipfile
import os
import shutil
import py7zr
import rarfile
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_warning(message):
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def print_success(message):
    print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}{message}{Style.RESET_ALL}")

def extract_file(file_path, extract_to):
    try:
        if file_path.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif file_path.endswith('.7z'):
            with py7zr.SevenZipFile(file_path, 'r') as archive:
                archive.extractall(path=extract_to)
        elif file_path.endswith('.rar'):
            with rarfile.RarFile(file_path) as archive:
                archive.extractall(path=extract_to)
        print_success(f"Extracted: {file_path}")
    except Exception as e:
        print_error(f"Failed to extract {file_path}: {e}")

def process_directory(src_dir, dest_dir):
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)
                shutil.move(file_path, os.path.join(dest_dir, file))
        for root, dirs, files in os.walk(src_dir):
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))
    except Exception as e:
        print_error(f"Failed to process directory: {src_dir}, Error: {e}")

def process_folder(folder_path, result_folder_path):
    temp_extracted_path = os.path.join(result_folder_path, os.path.basename(folder_path))
    process_directory(folder_path, temp_extracted_path)
    print_success(f"Processed folder: {folder_path}")

try:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Detect .zip, .rar, .7z files and folders in the same directory as the script
    items = [f for f in os.listdir(script_dir) if (f.endswith(('.zip', '.rar', '.7z')) or os.path.isdir(f)) and f not in ('Result', 'extracted_files')]

    # Check if there are any files or folders to process
    if not items:
        raise FileNotFoundError("No .zip, .rar, .7z files or folders found in the directory.")

    # Create the Result directory if it does not exist
    result_folder_path = os.path.join(script_dir, "Result")
    if not os.path.exists(result_folder_path):
        os.makedirs(result_folder_path)

    for item in items:
        item_path = os.path.join(script_dir, item)
        extracted_folder_path = os.path.join(script_dir, "extracted_files")

        if os.path.isdir(item_path):
            if item_path not in (result_folder_path, extracted_folder_path):
                process_folder(item_path, result_folder_path)
                shutil.rmtree(item_path)  # Delete the original folder
        else:
            # Create the directory for extracted files if it does not exist
            if not os.path.exists(extracted_folder_path):
                os.makedirs(extracted_folder_path)

            # Extract the file
            extract_file(item_path, extracted_folder_path)

            # Define original_file_name for use in final_dest_path
            original_file_name = os.path.basename(item_path)

            # Process the extracted directory
            final_dest_path = os.path.join(result_folder_path, os.path.splitext(original_file_name)[0])
            process_directory(extracted_folder_path, final_dest_path)

            # Remove the extracted_files directory as it is no longer needed
            shutil.rmtree(extracted_folder_path)

            # Print success message for the final processed directory
            print_success(f"Processed directory: {final_dest_path}")

            # Delete the original file
            os.remove(item_path)

except FileNotFoundError as e:
    print_error(f"Error: {e}")

except Exception as e:
    print_error(f"An unexpected error occurred: {e}")
