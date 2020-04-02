from flask import Flask
from flask_cors import CORS

import os

from restapi.config import Config
from restapi.data_generator import generate_random_data

# configure Flask
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# This needs to be here to avoid circular imports
from restapi.database import initialize_database

#loop that retries establishing a connection to the database until succeeds
DB_ESTABLISHED = False
while not DB_ESTABLISHED:
    try:
        initialize_database()
        DB_ESTABLISHED = True
        print("ESTABLISHED CONNECTION TO DB")
    except:
        continue


from restapi import routes

generate_random_data()
print('Done generating random data.')
