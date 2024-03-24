# Migration with APIs

This project demonstrates data migration using APIs. It includes scripts to import data from a CSV file into a temporary SQLite database, create a blank migration database, and start an API server to migrate data from the original database to the migration database.

## Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.x
- Flask (for the API server)

## Usage

1. **Start API Server:** Run `api_server.py` to start the API server for reading original data and writing to the migration database.

2. **Execute Migration Script:** Run `main.py` to execute the migration script, which fetches data from the original database using API endpoints and migrates it to the migration database.

## Scripts Overview

- **import_fake_data.py:** Imports data from `fake_data.csv` into a temporary SQLite database.

- **create_migration_db.py:** Creates a blank migration database with the required schema.

- **api_server_backend.py:** Defines the Flask API endpoints for fetching data, adding new items, and getting total rows.

- **main.py:** Executes the migration process by fetching data from API endpoints and migrating it to the migration database.

## Files

- **fake_data.csv:** Sample CSV file containing fake data for migration.

- **README.md:** This documentation file providing an overview of the project.

## Notes

- Ensure the API Server (`api_server.py`) is running before executing the migration script (`main.py`).

- The API Server runs on `http://127.0.0.1:5001/` by default. You can modify the base URL in `main.py` if needed.

## Error Logging

The migration script (`main.py`) logs errors encountered during API calls with status codes 400 and 500 to a temporary text file. The name of the error log file is printed at the end of script execution.
