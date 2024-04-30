import os
import re
import shutil
from send2trash import send2trash
import zipfile

def extract_zip(zip_file, extract_to):
    """Extracts the contents of a ZIP file."""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            zip_ref.extract(file_info, extract_to)

def process_logs(logs_dir, output_file):
    """Processes log files and logs matches."""
    matches = set()  # Set to store unique matches
    # Create logs directory if it doesn't exist
    os.makedirs(logs_dir, exist_ok=True)
    for root, _, files in os.walk(logs_dir):
        for file in files:
            if file.endswith(".log"):
                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if re.search(r'\.\./|/wp-login\.php\?action=register|403|install|select', line):
                            match = re.search(r'^([\d.]+),', line)
                            if match:
                                source_ip = match.group(1)
                                matches.add((source_ip, file))
    with open(output_file, 'w') as f:
        for ip, filename in matches:
            f.write(f"{ip},{filename}\n")

def rename_files(logs_dir):
    """Renames log files."""
    for root, _, files in os.walk(logs_dir):
        for file in files:
            if file.endswith(".log"):
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, f"processed_{file}")
                os.rename(old_path, new_path)

def delete_unmatched(logs_dir):
    """Deletes log files with no matches."""
    for root, dirs, files in os.walk(logs_dir):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                send2trash(dir_path)

def zip_logs(logs_dir, zip_file):
    """Zips up log files."""
    shutil.make_archive(os.path.splitext(zip_file)[0], 'zip', logs_dir)

def main(script_path):
    # Paths
    root_dir = os.path.dirname(os.path.realpath(script_path))
    log_processing_dir = os.path.join(root_dir, "log_processing")
    text_files_dir = os.path.join(root_dir, "text_files")
    logs_dir = os.path.join(log_processing_dir, "logs")
    access_logs_zip = os.path.join(text_files_dir, "access_logs.zip")
    results_zip = os.path.join(text_files_dir, "results.zip")
    matches_file = os.path.join(logs_dir, "matches.txt")

    # Create necessary directories
    os.makedirs(log_processing_dir, exist_ok=True)
    # Ensure logs directory is created before processing logs
    os.makedirs(logs_dir, exist_ok=True)

    # Extract ZIP file1
    extract_zip(access_logs_zip, logs_dir)

    # Process logs
    process_logs(logs_dir, matches_file)

    # Rename files
    rename_files(logs_dir)

    # Delete unmatched files
    delete_unmatched(logs_dir)

    # Zip log files
    zip_logs(logs_dir, results_zip)

if __name__ == "__main__":
    main(__file__)
