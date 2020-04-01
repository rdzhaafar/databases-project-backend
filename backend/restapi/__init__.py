from flask import Flask

from backend.restapi.config import Config

# configure Flask
app = Flask(__name__)
app.config.from_object(Config)

# This needs to be here to avoid circular imports
from backend.restapi.database import initialize_database

initialize_database()
from backend.restapi import routes
