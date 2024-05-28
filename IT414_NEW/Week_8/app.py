import csv
import pandas as pd
import sqlite3
import threading
import logging
import datetime
import requests
import os

# Define the correct path for the docs directory and log file
base_path = os.path.join('C:', os.sep, 'Users', 'Belay', 'IT414_Jschalte', 'IT414_NEW', 'Week_8')
docs_path = os.path.join(base_path, 'docs')
log_file_path = os.path.join(docs_path, 'script_log.txt')

# Ensure the docs folder exists before setting up logging
if not os.path.exists(docs_path):
    os.makedirs(docs_path)

# Configure logging
logging.basicConfig(filename=log_file_path, level=logging.INFO)

# Function to log task completion
def log_task(task_name):
    now = datetime.datetime.now().strftime("%B %d, %Y %H:%M:%S")
    logging.info(f"{now} - {task_name} is complete!")

# Function to download CSV file
def download_csv(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    log_task("CSV download")

# Function to generate Excel spreadsheet
def generate_excel(csv_file, excel_file):
    try:
        df = pd.read_csv(csv_file)
        df.to_excel(excel_file, index=False)
        log_task("Excel generation")
    except Exception as e:
        logging.error(f"Error generating Excel: {e}")

# Function to generate CSV for Google Sheet upload
def generate_google_sheet_csv(csv_file, google_sheet_csv_file):
    try:
        df = pd.read_csv(csv_file)
        df.to_csv(google_sheet_csv_file, index=False)
        log_task("Google Sheet CSV generation")
    except Exception as e:
        logging.error(f"Error generating Google Sheet CSV: {e}")

# Function to import data into database
def import_to_db(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS exam_data')
    cursor.execute('''CREATE TABLE exam_data (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        score INTEGER
                    )''')
    try:
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) == 2:
                    cursor.execute('INSERT INTO exam_data (name, score) VALUES (?, ?)', (row[0], row[1]))
                else:
                    logging.warning(f"Skipping invalid row: {row}")
        conn.commit()
        log_task("Database import")
    except Exception as e:
        logging.error(f"Error importing to database: {e}")
    finally:
        conn.close()

# Main function
def main():
    csv_url = 'https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week08/WI20-Assignment/exam_data.csv'
    csv_file = os.path.join(docs_path, 'exam_data.csv')
    excel_file = os.path.join(docs_path, 'exam_data.xlsx')
    google_sheet_csv_file = os.path.join(docs_path, 'exam_data_google_sheet.csv')
    db_file = os.path.join(docs_path, 'exam_data.db')

    # Create an empty log file or clear existing one
    open(log_file_path, 'w').close()

    download_csv(csv_url, csv_file)

    threads = []
    threads.append(threading.Thread(target=generate_excel, args=(csv_file, excel_file)))
    threads.append(threading.Thread(target=generate_google_sheet_csv, args=(csv_file, google_sheet_csv_file)))
    threads.append(threading.Thread(target=import_to_db, args=(csv_file, db_file)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()

