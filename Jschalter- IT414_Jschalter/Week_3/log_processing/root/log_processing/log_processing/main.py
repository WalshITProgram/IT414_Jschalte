import os
import shutil
import zipfile
import re
from send2trash import send2trash

def main():
    """Main function to perform the tasks described in the assignment."""
    # Step 1: Copy script to the root of any filesystem under log_processing folder
    copy_to_log_processing()

    # Step 2: Unzip data to logs folder preserving original structure
    unzip_to_logs()

    # Step 3: Process each log file
    process_logs()

    # Step 4: Zip the contents of logs folder
    zip_logs()

def copy_to_log_processing():
    """Copy the script to the root of any filesystem under log_processing folder."""
    script_path = os.path.abspath(__file__)
    destination_folder = os.path.join(os.path.dirname(script_path), "log_processing")
    os.makedirs(destination_folder, exist_ok=True)
    destination = os.path.join(destination_folder, os.path.basename(script_path))
    shutil.copy2(script_path, destination)

def unzip_to_logs():
    """Unzip the data to logs folder preserving original structure."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_file_path = os.path.join(script_dir, "text_files", "access_logs.zip")
    
    logs_dir = os.path.join(script_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(logs_dir)

def process_logs():
    """Process each log file, looking for specific patterns."""
    patterns = [r'([\d.]+)', r'\.\./', r'/wp-login\.php\?action=register', r' 403 ', r' install ', r' select ']
    ip_file_mapping = {}
    matches_file = os.path.join("logs", "matches.txt")

    for root, _, files in os.walk("logs"):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as log_file:
                for line in log_file:
                    for pattern in patterns:
                        match = re.search(pattern, line)
                        if match:
                            if pattern == patterns[0]:
                                ip = match.group(0)
                            else:
                                ip = match.group(1)
                                ip_file_mapping[ip] = file
                            break

    with open(matches_file, 'w') as matches:
        for ip, file in ip_file_mapping.items():
            matches.write(f"{ip}, {file}\n")

    # Step 5: Rename each log file
    for root, _, files in os.walk("logs"):
        for file in files:
            os.rename(os.path.join(root, file), os.path.join(root, f"processed_{file}"))

    # Step 6: Send files without matches to recycle bin
    for root, _, dirs in os.walk("logs"):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                send2trash(dir_path)

def zip_logs():
    """Zip the contents of logs folder into results.zip in text_files folder."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(script_dir, "logs")
    zip_path = os.path.join(script_dir, "text_files", "results.zip")
    shutil.make_archive(logs_dir, 'zip', logs_dir)
    os.rename(f"{logs_dir}.zip", zip_path)

if __name__ == "__main__":
    main()
