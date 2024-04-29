import os
import shutil

def create_destination_folder(destination: str):
    """Create the destination folder if it doesn't exist.

    Args:
        destination (str): The path to the destination folder.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)
        log_action(f"Folder created: {destination}")

def copy_files(source: str, destination: str):
    """Copy files from source to destination.

    Args:
        source (str): The path to the source folder.
        destination (str): The path to the destination folder.
    """
    for root, dirs, files in os.walk(source):
        for file in files:
            source_file = os.path.join(root, file)
            if os.path.getsize(source_file) <= 1e9:  # 1 GB limit
                try:
                    relative_path = os.path.relpath(root, source)
                    destination_folder = os.path.join(destination, relative_path)
                    destination_file = os.path.join(destination_folder, file)
                    
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    shutil.copy2(source_file, destination_file)
                    log_action(f"File copied: {file} to {destination_file}")
                except Exception as e:
                    log_action(f"Error copying {file}: {str(e)}")
            else:
                log_action(f"Skipped: {file} (file size exceeds 1 GB)")

def log_action(action: str):
    """Log actions to log.txt file.

    Args:
        action (str): The action to be logged.
    """
    with open("log.txt", "a") as log_file:
        log_file.write(action + "\n")

def main():
    source = input("Enter the source folder: ")
    destination = input("Enter the destination folder: ")

    # Check if source folder exists
    if not os.path.exists(source):
        print("Source folder does not exist.")
        return

    create_destination_folder(destination)

    try:
        copy_files(source, destination)
    except Exception as e:
        print("An error occurred:", str(e))
    else:
        print("Copy operation completed successfully.")

if __name__ == "__main__":
    main()