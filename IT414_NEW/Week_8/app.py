import csv
import pandas as pd
import sqlite3
import threading
import logging
import datetime
import requests
import os

# Configure logging
log_file_path = os.path.join('docs', 'script_log.txt')
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
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False)
    log_task("Excel generation")

# Function to generate Google Sheet
def generate_google_sheet(csv_file):
    # Assuming credentials and sheet setup is handled
    # Code to interact with Google Sheets API to create a sheet
    log_task("Google Sheet generation")

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

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            cursor.execute('INSERT INTO exam_data (name, score) VALUES (?, ?)', (row[0], row[1]))

    conn.commit()
    conn.close()
    log_task("Database import")

# Main function
def main():
    csv_url = 'https://github.com/WalshITProgram/IT414_Jschalte/blob/main/IT414_NEW/Week_8/exam_data.csv'
    csv_file = 'exam_data.csv'
    excel_file = 'exam_data.xlsx'
    db_file = 'exam_data.db'

    # Ensure the docs folder exists
    if not os.path.exists('docs'):
        os.makedirs('docs')

    # Create an empty log file or clear existing one
    open(log_file_path, 'w').close()

    download_csv(csv_url, csv_file)

    threads = []
    threads.append(threading.Thread(target=generate_excel, args=(csv_file, excel_file)))
    threads.append(threading.Thread(target=generate_google_sheet, args=(csv_file,)))
    threads.append(threading.Thread(target=import_to_db, args=(csv_file, db_file)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
