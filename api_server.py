# coding=utf-8
# Migration with API's
# Marcelo Ambrosio de Góes
# 2024-03-24

from import_fake_data import *
from create_migration_db import *
from api_server_backend import *

# Import fake_data.csv to a temporary SQLite database
fake_data_db = import_fake_data()
# Create a blank database to migrate data to
migration_db_blank = create_migration_db()
# Start API server to read original data and write to migration database
api_server(fake_data_db, migration_db_blank)
