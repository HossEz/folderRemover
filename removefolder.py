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

def print_info(message):
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

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
        print_success(f"Extracted: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print_error(f"Failed to extract {os.path.basename(file_path)}: {e}")
        return False

def process_directory(src_dir, dest_dir):
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        
        files_moved = 0
        for root, dirs, files in os.walk(src_dir):
            for file in files:
                file_path = os.path.join(root, file)
                dest_file = os.path.join(dest_dir, file)
                
                # Handle duplicate filenames
                counter = 1
                while os.path.exists(dest_file):
                    name, ext = os.path.splitext(file)
                    dest_file = os.path.join(dest_dir, f"{name}_{counter}{ext}")
                    counter += 1
                
                shutil.move(file_path, dest_file)
                files_moved += 1
        
        # Clean up empty directories
        for root, dirs, files in os.walk(src_dir, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):  # Only remove if empty
                        os.rmdir(dir_path)
                except OSError:
                    pass  # Directory not empty or other error
        
        return files_moved
    except Exception as e:
        print_error(f"Failed to process directory: {src_dir}, Error: {e}")
        return 0

def process_folder(folder_path, result_folder_path):
    temp_extracted_path = os.path.join(result_folder_path, os.path.basename(folder_path))
    files_moved = process_directory(folder_path, temp_extracted_path)
    print_success(f"Processed folder: {os.path.basename(folder_path)} ({files_moved} files moved)")

def main():
    try:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Extended blacklist of folders and files to ignore
        blacklist = {
            'Result', 'extracted_files', '.venv', 'venv', '__pycache__', 
            '.git', '.vs', '.vscode', 'node_modules', '.env',
            'requirements.txt', 'removefolder.py', os.path.basename(__file__)
        }
        
        # Also blacklist any .bat files
        all_items = os.listdir(script_dir)
        for item in all_items:
            if item.endswith('.bat'):
                blacklist.add(item)

        print_info(f"Scanning directory: {script_dir}")
        print_info(f"Ignoring: {', '.join(sorted(blacklist))}")
        print()

        # Detect .zip, .rar, .7z files and folders in the same directory as the script
        items = []
        for item in all_items:
            item_path = os.path.join(script_dir, item)
            if item not in blacklist:
                if item.endswith(('.zip', '.rar', '.7z')) or os.path.isdir(item_path):
                    items.append(item)

        # Check if there are any files or folders to process
        if not items:
            print_warning("No .zip, .rar, .7z files or folders found to process.")
            print_info("Place archive files or folders in the same directory as this script.")
            return

        print_info(f"Found {len(items)} items to process:")
        for item in items:
            item_path = os.path.join(script_dir, item)
            if os.path.isdir(item_path):
                print_info(f"  📁 {item}")
            else:
                print_info(f"  📦 {item}")
        print()

        # Create the Result directory if it does not exist
        result_folder_path = os.path.join(script_dir, "Result")
        if not os.path.exists(result_folder_path):
            os.makedirs(result_folder_path)
            print_success("Created 'Result' directory")

        total_processed = 0
        
        for item in items:
            item_path = os.path.join(script_dir, item)
            extracted_folder_path = os.path.join(script_dir, "extracted_files")

            if os.path.isdir(item_path):
                print_info(f"Processing folder: {item}")
                process_folder(item_path, result_folder_path)
                shutil.rmtree(item_path)  # Delete the original folder
                total_processed += 1
            else:
                print_info(f"Processing archive: {item}")
                
                # Create the directory for extracted files if it does not exist
                if not os.path.exists(extracted_folder_path):
                    os.makedirs(extracted_folder_path)

                # Extract the file
                if extract_file(item_path, extracted_folder_path):
                    # Define original_file_name for use in final_dest_path
                    original_file_name = os.path.basename(item_path)

                    # Process the extracted directory
                    final_dest_path = os.path.join(result_folder_path, os.path.splitext(original_file_name)[0])
                    files_moved = process_directory(extracted_folder_path, final_dest_path)

                    # Remove the extracted_files directory as it is no longer needed
                    if os.path.exists(extracted_folder_path):
                        shutil.rmtree(extracted_folder_path)

                    # Print success message for the final processed directory
                    print_success(f"Processed archive: {original_file_name} ({files_moved} files extracted)")

                    # Delete the original file
                    os.remove(item_path)
                    total_processed += 1
                else:
                    print_warning(f"Skipping {item} due to extraction failure")

        print()
        print_success(f"✅ Processing complete! {total_processed} items processed successfully.")
        print_info(f"📂 Results saved to: {result_folder_path}")

    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        import traceback
        print_error(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()