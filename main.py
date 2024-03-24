# coding=utf-8
# Migration with API's
# Marcelo Ambrosio de Góes
# 2024-03-24

# Please ensure that the API Server (api_server.py) is running before executing

import requests
import time
import tempfile

# Define the base URL for the API endpoints
base_url = 'http://127.0.0.1:5001/'

# Define the specific endpoints
total_rows_endpoint = 'user/total_rows'
row_endpoint = 'user/row/'
add_item_endpoint = 'add_item'

# Create a temporary file to log errors
error_log_file = tempfile.NamedTemporaryFile(mode='w', delete=False)

# Get the total number of rows
total_rows_url = base_url + total_rows_endpoint
response_total_rows = requests.get(total_rows_url)
total_rows_data = response_total_rows.json()
total_rows = total_rows_data.get('total_rows', 0)

# Execute GET requests for each row (original database) and then POST to add_item endpoint (migrated database)
for row_number in range(1, total_rows + 1):
    # Execute GET request to fetch data for each row
    row_url = base_url + row_endpoint + str(row_number)
    row_response = requests.get(row_url)
    row_data = row_response.json()

    # Extract data from the response
    balance = row_data.get('balance')
    name = row_data.get('name')
    original_id = row_data.get('original_id')

    # Execute POST request to add_item endpoint
    add_item_url = base_url + add_item_endpoint
    data = {'balance': balance, 'name': name, 'original_id': original_id}
    response_add_item = requests.post(add_item_url, json=data)

    # Log errors to the temporary text file
    if response_add_item.status_code in [400, 500]:
        error_log_file.write(f'Error for row {row_number}: {response_add_item.json()}\n')

    # Print the response for each row
    print(f'Response for row {row_number}: {response_add_item.json()}')

    # Sleep for 0.1 seconds
    time.sleep(0.1)

# Close the error log file
error_log_file.close()

# Print the name of the error log file
print(f'Error log file: {error_log_file.name}')

