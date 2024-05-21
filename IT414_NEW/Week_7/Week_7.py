import os
import zipfile
import sqlite3
import pandas as pd
import json
import xml.etree.ElementTree as ET

def create_tables(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS addresses_working (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip TEXT
        )
    ''')
    conn.commit()
    conn.close()

def extract_sample_data(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def import_csv(file_path):
    return pd.read_csv(file_path)

def import_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def import_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for elem in root:
        record = {}
        for subelem in elem:
            record[subelem.tag] = subelem.text
        data.append(record)
    return pd.DataFrame(data)

def import_data(file_path, file_type):
    if file_type == 'csv':
        return import_csv(file_path)
    elif file_type == 'json':
        return import_json(file_path)
    elif file_type == 'xml':
        return import_xml(file_path)
    else:
        raise ValueError("Unsupported file type")

def swap_tables(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("BEGIN TRANSACTION")
    cursor.execute("ALTER TABLE addresses RENAME TO addresses_old")
    cursor.execute("ALTER TABLE addresses_working RENAME TO addresses")
    cursor.execute("ALTER TABLE addresses_old RENAME TO addresses_working")
    cursor.execute("COMMIT")
    conn.close()

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_name = os.path.join(current_dir, 'address_data.db')
    sample_data_zip = os.path.join(current_dir, 'sample_data.zip')
    extract_to = os.path.join(current_dir, 'sample_data')
    
    create_tables(db_name)
    extract_sample_data(sample_data_zip, extract_to)
    
    file_name = input("Enter the file name to import (with extension): ")
    file_path = os.path.join(extract_to, file_name)
    
    if not os.path.exists(file_path):
        print("File does not exist")
        return
    
    file_type = file_name.split('.')[-1]
    
    try:
        data = import_data(file_path, file_type)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM addresses_working")
        data.to_sql('addresses_working', conn, if_exists='append', index=False)
        swap_tables(db_name)
        conn.close()
        print("Import complete")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
