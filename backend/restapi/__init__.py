from flask import Flask

import os

from restapi.config import Config

# configure Flask
app = Flask(__name__)
app.config.from_object(Config)

# This needs to be here to avoid circular imports
from restapi.database import initialize_database

#loop that retries establishing a connection to the database until succeeds
while True:
    try:
        initialize_database()
        break
    except:
        continue


from restapi import routes
