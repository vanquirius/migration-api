# coding=utf-8
# Migration with API's
# Marcelo Ambrosio de Góes
# 2024-03-24

import sqlite3
import tempfile


def create_migration_db():
    # Create a temporary SQLite database
    temp_db = tempfile.NamedTemporaryFile(delete=False)
    db_conn = sqlite3.connect(temp_db.name, detect_types=sqlite3.PARSE_DECLTYPES)
    cursor = db_conn.cursor()

    # Create a new blank table with new_id, original_id, name, and balance columns
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            new_id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_id INTEGER,
            name TEXT,
            balance REAL
        );
    '''
    cursor.execute(create_table_query)

    # Commit the changes and close the database connection
    db_conn.commit()
    db_conn.close()

    # Print the path to the temporary SQLite database
    print("Migration SQLite database created at: " + temp_db.name)

    return temp_db.name
