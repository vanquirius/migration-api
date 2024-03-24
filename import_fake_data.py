# coding=utf-8
# Migration with API's
# Marcelo Ambrosio de Góes
# 2024-03-24

import sqlite3
import csv
import tempfile


def import_fake_data():
    # Define the CSV file path
    csv_file = "fake_data.csv"

    # Create a temporary SQLite database
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    db_conn = sqlite3.connect(temp_db.name)
    cursor = db_conn.cursor()

    # Create a table to store the data
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            original_id INTEGER,
            name TEXT,
            balance REAL
        );
    '''
    cursor.execute(create_table_query)

    # Read data from the CSV file and insert into the database
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            original_id = int(row['original_id'])
            name = row['name']
            balance = float(row['balance'])
            insert_query = '''
                INSERT INTO users (original_id, name, balance)
                VALUES (?, ?, ?)
            '''
            cursor.execute(insert_query, (original_id, name, balance))

    # Commit the changes and close the database connection
    db_conn.commit()
    db_conn.close()

    # Print the path to the temporary SQLite database
    print("Original data SQLite database created at: " + temp_db.name)

    return temp_db.name
