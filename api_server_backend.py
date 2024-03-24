# coding=utf-8
# Migration with API's
# Marcelo Ambrosio de Góes
# 2024-03-24

from flask import Flask, request, jsonify, g
import sqlite3
import os


def api_server(original_data_db, migration_db):
    app = Flask(__name__)

    # Get the SQLite connection - original data
    def get_db_original_data():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(original_data_db)
            # Set charset to UTF-8
            db.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
            db.text_factory = lambda x: str(x, 'utf-8', 'ignore') if isinstance(x, bytes) else str(x)
        return db

    # Close the SQLite connection after each request
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    # Get the SQLite connection - migration data
    def get_db_migration_data():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(migration_db, detect_types=sqlite3.PARSE_DECLTYPES)
            db.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
            db.text_factory = lambda x: str(x, 'utf-8', 'ignore') if isinstance(x, bytes) else str(
                x)  # Set charset to UTF-8
        return db

    # Endpoint to fetch a specific row based on row number
    @app.route('/user/row/<int:row_num>', methods=['GET'])
    def get_user_by_row(row_num):
        try:
            # Get the SQLite connection
            db_conn = get_db_original_data()
            cursor = db_conn.cursor()

            # Query the database for the specified row number
            query = 'SELECT * FROM users WHERE ROWID = ?'
            cursor.execute(query, (row_num,))
            user_data = cursor.fetchone()

            if user_data:
                # Convert the database row to a dictionary
                user_dict = {
                    'original_id': user_data[0],
                    'name': user_data[1],
                    'balance': user_data[2]
                }
                return jsonify(user_dict), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Endpoint to fetch the total number of rows in the users table
    @app.route('/user/total_rows', methods=['GET'])
    def get_total_rows():
        try:
            # Get the SQLite connection
            db_conn = get_db_original_data()
            cursor = db_conn.cursor()

            # Query to count the total number of rows
            query = 'SELECT COUNT(*) FROM users'
            cursor.execute(query)
            total_rows = cursor.fetchone()[0]

            return jsonify({'total_rows': total_rows}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    import re

    # Endpoint to add new items to the database
    @app.route('/add_item', methods=['POST'])
    def add_item():
        try:
            data = request.get_json()
            name = data.get('name')
            balance = data.get('balance')
            original_id = data.get('original_id')

            if not name or not balance:
                return jsonify({'error': 'Name and balance fields are mandatory'}), 400

            # Check if name contains emoji
            if re.search(
                    r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251\U0001f926-\U0001f937\U0001F1E0-\U0001F1FF]+',
                    name):
                return jsonify({'error': 'Name should not contain emojis'}), 400

            db = get_db_migration_data()
            cursor = db.cursor()

            # Insert data into the database
            if original_id:
                insert_query = '''
                    INSERT INTO users (original_id, name, balance)
                    VALUES (?, ?, ?)
                '''
                cursor.execute(insert_query, (original_id, name, balance))
            else:
                insert_query = '''
                    INSERT INTO users (name, balance)
                    VALUES (?, ?)
                '''
                cursor.execute(insert_query, (name, balance))
            db.commit()

            # Get the last inserted row ID (new_id)
            new_id = cursor.lastrowid

            # Fetch the inserted data from the database
            cursor.execute('SELECT * FROM users WHERE new_id = ?', (new_id,))
            row = cursor.fetchone()

            if row:
                # Construct a verbose response with all column values
                response = {
                    'message': 'Item added successfully',
                    'new_id': row[0],
                    'original_id': row[1],
                    'name': row[2],
                    'balance': row[3]
                }
                return jsonify(response), 200
            else:
                return jsonify({'error': 'Failed to fetch inserted data'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # Enable UTF-8 for Flask
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    app.run(debug=True, port=5001)
